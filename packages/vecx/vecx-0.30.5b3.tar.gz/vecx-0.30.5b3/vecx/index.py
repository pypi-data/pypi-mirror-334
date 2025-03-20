import requests, json, zlib
import numpy as np
from google.protobuf.json_format import Parse, MessageToJson
from .libvx import LibVectorX as Vxlib
from .crypto import get_checksum,json_zip,json_unzip
from .exceptions import raise_exception
from .vecx_pb2 import VectorObject, VectorBatch, ResultSet, VectorResult

class Index:
    def __init__(self, name:str, key:str, token:str, url:str, version:int=1, params=None):
        self.name = name
        self.key = key
        self.token = token
        self.url = url
        self.version = version
        self.checksum = get_checksum(self.key)
        self.lib_token = params["lib_token"]
        self.count = params["total_elements"]
        self.space_type = params["space_type"]
        self.dimension = params["dimension"]
        self.precision = "float16" if params["use_fp16"] else "float32"
        self.M = params["M"]

        if key:
            self.vxlib = Vxlib(key=key, lib_token=self.lib_token, space_type=self.space_type, version=version, dimension=self.dimension)
        else:
            self.vxlib = None

    def __str__(self):
        return self.name
    
    def _normalize_vector(self, vector):
        # Normalize only if using cosine distance
        if self.space_type != "cosine":
            return vector, 1.0
        vector = np.array(vector, dtype=np.float32)
        norm = np.linalg.norm(vector)
        if norm == 0:
            return vector, 1.0
        normalized_vector = vector / norm
        return normalized_vector, float(norm)

    # def upsert(self, input_array):
    #     import concurrent.futures
    #     from math import ceil
        
    #     if len(input_array) > 4000:
    #         raise ValueError("Cannot insert more than 4000 vectors at a time")
        
    #     # If the array is small, process it directly
    #     if len(input_array) <= 1000:
    #         return self._process_batch(input_array)
        
    #     # For larger arrays, split into 4 batches and process in parallel
    #     batch_size = ceil(len(input_array) / 4)
    #     batches = [input_array[i:i + batch_size] for i in range(0, len(input_array), batch_size)]
        
    #     # Use ThreadPoolExecutor to process batches in parallel
    #     with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    #         # Submit all batches for processing
    #         future_to_batch = {executor.submit(self._process_batch, batch): i for i, batch in enumerate(batches)}
            
    #         # Process results as they complete
    #         for future in concurrent.futures.as_completed(future_to_batch):
    #             batch_index = future_to_batch[future]
    #             try:
    #                 result = future.result()
    #                 # We could log success for each batch if needed
    #                 # print(f"Batch {batch_index} completed successfully")
    #             except Exception as exc:
    #                 # If any batch fails, propagate the exception
    #                 raise ValueError(f"Batch {batch_index} generated an exception: {exc}")
        
    #     return "Vectors inserted successfully"

    # def _process_batch(self, batch):
    #     """Process a single batch of vectors and send to server"""
    #     vector_batch = VectorBatch()
        
    #     for item in batch:
    #         # Prepare vector object
    #         vector_obj = VectorObject()
    #         vector_obj.id = str(item.get('id', ''))
    #         vector_obj.filter = json.dumps(item.get('filter', ""))
    #         # Meta is zipped
    #         meta = json_zip(dict=item.get('meta', ""))
    #         vector, norm = self._normalize_vector(item['vector'])
    #         vector_obj.norm = norm
    #         # Encrypt vector and meta only if checksum is valid
    #         if self.vxlib:
    #             vector = self.vxlib.encrypt_vector(vector)
    #             meta = self.vxlib.encrypt_meta(meta)
    #         vector_obj.meta = meta
    #         vector_obj.vector.extend(vector)

    #         # Add to batch
    #         vector_batch.vectors.append(vector_obj)
        
    #     # Serialize batch
    #     serialized_data = vector_batch.SerializeToString()
        
    #     # Prepare headers
    #     headers = {
    #         'Authorization': self.token,
    #         'Content-Type': 'application/x-protobuf'
    #     }

    #     # Send request
    #     response = requests.post(
    #         f'{self.url}/index/{self.name}/vector/batch', 
    #         headers=headers, 
    #         data=serialized_data
    #     )

    #     if response.status_code != 200:
    #         raise_exception(response.status_code, response.text)

    #     return "Batch processed successfully"
        
    def upsert(self, input_array):
        import concurrent.futures
        from math import ceil
        import time
        
        start_time = time.time()
        print(f"upsert called with {len(input_array)} vectors")
        
        if len(input_array) > 4000:
            raise ValueError("Cannot insert more than 4000 vectors at a time")
        
        # If the array is small, process it directly
        if len(input_array) <= 1000:
            print("Processing small batch directly")
            result = self._process_batch(input_array)
            print(f"Small batch completed in {time.time() - start_time:.2f} seconds")
            return result
        
        # For larger arrays, split into 4 batches and process in parallel
        batch_size = ceil(len(input_array) / 4)
        batches = [input_array[i:i + batch_size] for i in range(0, len(input_array), batch_size)]
        print(f"Split into {len(batches)} batches of approximately {batch_size} vectors each")
        
        batch_times = {}
        batch_starts = {}
        
        # Use ProcessPoolExecutor instead of ThreadPoolExecutor to process batches in parallel
        with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
            # Submit all batches for processing
            print(f"Submitting batches at {time.time() - start_time:.2f} seconds")
            future_to_batch = {executor.submit(self._process_batch, batch): i for i, batch in enumerate(batches)}
            for i in range(len(batches)):
                batch_starts[i] = time.time()
            
            # Process results as they complete
            for future in concurrent.futures.as_completed(future_to_batch):
                batch_index = future_to_batch[future]
                batch_end_time = time.time()
                batch_duration = batch_end_time - batch_starts[batch_index]
                batch_times[batch_index] = batch_duration
                print(f"Batch {batch_index} completed in {batch_duration:.2f} seconds")
                
                try:
                    result = future.result()
                    # We could log success for each batch if needed
                except Exception as exc:
                    print(f"Batch {batch_index} failed after {batch_duration:.2f} seconds with error: {exc}")
                    # If any batch fails, propagate the exception
                    raise ValueError(f"Batch {batch_index} generated an exception: {exc}")
        
        # This is the synchronization point - we don't proceed until all batches are done
        sync_time = time.time()
        print(f"All batches completed. Synchronization point reached at {sync_time - start_time:.2f} seconds")
        print(f"Batch completion times: {batch_times}")
        print(f"Slowest batch took {max(batch_times.values()):.2f} seconds")
        print(f"Fastest batch took {min(batch_times.values()):.2f} seconds")
        
        end_time = time.time()
        print(f"upsert completed in {end_time - start_time:.2f} seconds")
        
        return "Vectors inserted successfully"

    def _process_batch(self, batch):
        """Process a single batch of vectors and send to server"""
        import time
        start_time = time.time()
        print(f"Processing batch of {len(batch)} vectors")
        
        # Timing for protobuf creation
        proto_start = time.time()
        vector_batch = VectorBatch()
        
        for item in batch:
            # Prepare vector object
            vector_obj = VectorObject()
            vector_obj.id = str(item.get('id', ''))
            vector_obj.filter = json.dumps(item.get('filter', ""))
            # Meta is zipped
            meta = json_zip(dict=item.get('meta', ""))
            vector, norm = self._normalize_vector(item['vector'])
            vector_obj.norm = norm
            # Encrypt vector and meta only if checksum is valid
            if self.vxlib:
                vector = self.vxlib.encrypt_vector(vector)
                meta = self.vxlib.encrypt_meta(meta)
            vector_obj.meta = meta
            vector_obj.vector.extend(vector)

            # Add to batch
            vector_batch.vectors.append(vector_obj)
        
        proto_end = time.time()
        print(f"Protobuf creation took {proto_end - proto_start:.2f} seconds for {len(batch)} vectors")
        
        # Serialize batch
        serialize_start = time.time()
        serialized_data = vector_batch.SerializeToString()
        serialize_end = time.time()
        print(f"Serialization took {serialize_end - serialize_start:.2f} seconds")
        
        # Prepare headers
        headers = {
            'Authorization': self.token,
            'Content-Type': 'application/x-protobuf'
        }

        # Send request
        request_start = time.time()
        print(f"Sending request with {len(batch)} vectors, size: {len(serialized_data)} bytes")
        response = requests.post(
            f'{self.url}/index/{self.name}/vector/batch', 
            headers=headers, 
            data=serialized_data
        )
        request_end = time.time()
        print(f"Request completed in {request_end - request_start:.2f} seconds")

        if response.status_code != 200:
            raise_exception(response.status_code, response.text)
        
        print(f"Batch processing completed in {time.time() - start_time:.2f} seconds")
        return "Batch processed successfully"

    def query(self, vector, top_k=10, filter=None, include_vectors=False, log=False):
        if top_k > 100:
            raise ValueError("top_k cannot be greater than 100")
        checksum = get_checksum(self.key)

        # Normalize query vector if using cosine distance
        norm=1.0
        if self.space_type == "cosine":
            vector, norm = self._normalize_vector(vector)

        original_vector = vector
        if self.vxlib:
            vector = self.vxlib.encrypt_vector(vector)
            top_k += 5  # Add some extra results for over-fetching and re-scoring
        headers = {
            'Authorization': f'{self.token}',
            'Content-Type': 'application/json'
        }
        data = {
            'vector': vector.tolist(),
            'k': top_k,
            'include_vectors': include_vectors
        }
        if filter:
            data['filter'] = json.dumps(filter)
        response = requests.post(f'{self.url}/index/{self.name}/search', headers=headers, json=data)
        if response.status_code != 200:
            raise_exception(response.status_code, response.text)

        # Parse protobuf ResultSet
        result_set = ResultSet()
        result_set.ParseFromString(response.content)

        # Convert to a more Pythonic list of dictionaries
        vectors = []
        processed_results = []
        for result in result_set.results:
            processed_result = {
                'id': result.id,
                'distance': result.distance,
                'similarity': 1 - result.distance,
                'meta': json_unzip(self.vxlib.decrypt_meta(result.meta)) if self.vxlib else json_unzip(result.meta),
            }
            # Filter will come as "" - default value in protobuf
            if filter != "":
                processed_result['filter'] = json.loads(result.filter)

            # Include vector if requested and available
            if include_vectors or self.vxlib:
                processed_result['vector'] = list(self.vxlib.decrypt_vector(result.vector)) if self.vxlib else list(result.vector)
                vectors.append(np.array(processed_result['vector'],dtype=np.float32))

            processed_results.append(processed_result)
        
        # If using encryption, rescore the results
        top_k -= 5
        if self.vxlib:
            distances = self.vxlib.calculate_distances(query_vector=original_vector,vectors=vectors)
            # Set distace and similarity in processed results
            for i, result in enumerate(processed_results):
                result['distance'] = distances[i]
                result['similarity'] = 1 - distances[i]
            # Now sort processed results by distance inside processed result
            processed_results = sorted(processed_results, key=lambda x: x['distance'])
            # Return only top_k results
            processed_results = processed_results[:top_k]
            #print(distances)
            # If include_vectors is False then remove the vectors from the result
            if not include_vectors:
                for result in processed_results:
                    result.pop('vector', None)

        return processed_results

    def delete_vector(self, id):
        checksum = get_checksum(self.key)
        headers = {
            'Authorization': f'{self.token}',
            }
        response = requests.delete(f'{self.url}/index/{self.name}/vector/{id}/delete', headers=headers)
        if response.status_code != 200:
            raise_exception(response.status_code)
        return response.text + " rows deleted"
    
    # Delete multiple vectors based on a filter
    def delete_with_filter(self, filter):
        checksum = get_checksum(self.key)
        headers = {
            'Authorization': f'{self.token}',
            'Content-Type': 'application/json'
            }
        data = {"filter": filter}
        print(filter)
        response = requests.delete(f'{self.url}/index/{self.name}/vectors/delete', headers=headers, json=data)
        if response.status_code != 200:
            print(response.text)
            raise_exception(response.status_code)
        return response.text
    
    def describe(self):
        data = {
            "name": self.name,
            "space_type": self.space_type,
            "dimension": self.dimension,
            "count": self.count,
            "precision": self.precision,
            "M": self.M,
        }
        return data

