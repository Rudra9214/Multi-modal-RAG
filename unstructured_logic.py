from dotenv import load_dotenv

import os

from unstructured_ingest.v2.pipeline.pipeline import Pipeline

from unstructured_ingest.v2.interfaces import ProcessorConfig

from unstructured_ingest.v2.processes.connectors.local import (

    LocalIndexerConfig,

    LocalDownloaderConfig,

    LocalConnectionConfig,

    LocalUploaderConfig

)

from unstructured_ingest.v2.processes.partitioner import PartitionerConfig

from unstructured_ingest.v2.processes.chunker import ChunkerConfig

from unstructured.staging.base import elements_from_json

 

def load_processed_files(directory_path):

    elements = []

    for filename in os.listdir(directory_path):

        if filename.endswith('.json'):

            file_path = os.path.join(directory_path, filename)

            try:

                elements.extend(elements_from_json(filename=file_path))

            except IOError:

                print(f"Error: Could not read file {filename}.")

    return elements

 

if __name__ == '__main__':

    load_dotenv()

 

    # Update paths to absolute paths

    directory_with_pdfs = r"c:\Users\rudraraj.thakar\Desktop\PDF_parser\sample06.pdf"

    directory_with_results = r"c:\Users\rudraraj.thakar\Desktop\PDF_parser"

 

    # Ensure the output directory exists

    os.makedirs(directory_with_results, exist_ok=True)

 

    Pipeline.from_configs(

        context=ProcessorConfig(),

        indexer_config=LocalIndexerConfig(input_path=directory_with_pdfs),

        downloader_config=LocalDownloaderConfig(),

        source_connection_config=LocalConnectionConfig(),

        partitioner_config=PartitionerConfig(

            partition_by_api=True,

            api_key=os.getenv("UNSTRUCTURED_API_KEY"),

            partition_endpoint=os.getenv("UNSTRUCTURED_API_URL"),

            strategy="hi_res",

            additional_partition_args={

                "split_pdf_page": True,

                "split_pdf_concurrency_level": 15,

            },

        ),

        uploader_config=LocalUploaderConfig(output_dir=directory_with_results)

    ).run()

 

    # elements = load_processed_files(directory_with_results)
