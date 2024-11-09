from langchain.prompts import PromptTemplate, ChatPromptTemplate

from langchain_openai import ChatOpenAI

from langchain_community.document_loaders import JSONLoader

from langchain.chains import LLMChain

from langchain.text_splitter import RecursiveCharacterTextSplitter

import os

from dotenv import load_dotenv

 

load_dotenv()




# Define the prompt for detecting signatures in the document

chat_prompt = """\

You are an advanced document analysis tool designed to extract electronic signatures. Your task is to find the name of the signer immediately after the following keywords or similar:

 

- "DocuSigned by"

- "Signer Name"

- "Signed by"

- "Electronically signed by"

- "Digitally Signed by"

- "Signed By"

 

For each document, return the following:

 

- **Number of signatures**: The count of signers found.

- **Signatures**: A list of names.

 

### Input:

{document_text}

 

### Output format:

Number of signatures: X

Signatures:

1. Name of signer 1

2. Name of signer 2

..."""

 

document_path = r'c:\Users\rudraraj.thakar\Desktop\PDF_parser\sample06.pdf.json'

loader = JSONLoader(file_path=document_path, jq_schema=".[]", text_content=False)

document = loader.load()

 

# Initialize the LLM model

llm = ChatOpenAI(model="gpt-4o")

 

# Define the LLM chain for processing the document text

prompt = ChatPromptTemplate.from_messages([("system", "{system}"), ("human", "{input}")])

 

# Sample input document (replace this with a JSON loading step if necessary)

document_text = " ".join([str(doc['page_content']) if isinstance(doc, dict) else str(doc) for doc in document])

 

# Split the document text (optional, depending on the size of the input)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=100)

chunks = text_splitter.split_text(document_text)

 

# Initialize response storage

responses = []

 

# Initialize variables to keep track of the signatures

signature_count = 0

signers = []

 

# Iterate through chunks

for chunk in chunks:

    input_data = {

        "system": chat_prompt,

        "input": chunk

    }

   

    # Create the LLM chain and invoke the model

    signature_chain = prompt | llm

    response = signature_chain.invoke(input_data)

   

    # Print the raw response content for debugging

    #print(f"Response: {response.content}")

   

    # Parse the response to extract the number of signatures and the signers' names

    response_content = response.content.strip().split("\n")

   

    # Look for the "Number of signatures" line

    for line in response_content:

        if line.startswith("Number of signatures:"):

            # Extract the number of signatures

            signature_count += int(line.split(":")[1].strip())

       

        # Look for the "Signatures" section

        elif line.startswith("1.") or line.startswith("2.") or line.startswith("3.") or line.startswith("4."):

            # Extract the name of the signer (assumes the format "1. Name")

            signer_name = line.split(".", 1)[1].strip()

            signers.append(signer_name)

 

    # Print the ongoing results for debugging purposes

    '''print(f"Total Signatures Found so far: {signature_count}")

    print("Signers so far:")

    for idx, signer in enumerate(signers, 1):

        print(f"{idx}. {signer}")'''

 

# Final output after processing all chunks

print(f"Final Number of Signatures: {signature_count}")

print("Final List of Signers:")

for idx, signer in enumerate(signers, 1):

    print(f"{idx}. {signer}")
