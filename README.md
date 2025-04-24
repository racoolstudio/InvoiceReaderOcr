# InvoiceReaderOCR

InvoiceReaderOCR is a Python-based Optical Character Recognition (OCR) API designed to extract key information from invoice images. It identifies critical invoice details such as vendor name, invoice number, invoice date, due date, and PO number. Additionally, it extracts tabular data from the invoices and returns the results in a structured JSON format.

## Features

- **Vendor Detection**: Automatically detects and identifies the vendor name from the invoice.
- **Invoice Data Extraction**: Extracts key details such as:
  - Invoice Number
  - Invoice Date
  - Due Date
  - Purchase Order (PO) Number
- **Tabular Data Extraction**: Processes invoice tables and retrieves itemized data.
- **API Integration**: Exposes an easy-to-use REST API for integration with other systems.

## Getting Started

### Prerequisites

- Python 3.8+ (if not using Docker)
- Docker (optional, recommended for simplified setup)

### Installation

#### Option 1: Running Locally

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/InvoiceReaderOCR.git
    cd InvoiceReaderOCR
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Start the server**:
    ```bash
    python app.py
    ```

4. The application will run on `http://localhost:5000`.

#### Option 2: Running with Docker

1. **Build the Docker image**:
    ```bash
    docker build -t invoice-reader-ocr .
    ```

2. **Run the Docker container**:
    ```bash
    docker run -p 5000:5000 invoice-reader-ocr
    ```

3. The application will run on `http://localhost:5000`.

### API Endpoints

#### 1. Home Endpoint
- **URL**: `/`
- **Method**: `GET`
- **Description**: Returns a welcome message.
- **Response**:
    ```json
    {
        "message": "Hello, and Welcome to the OCR API!"
    }
    ```

#### 2. Get All Invoice Details
- **URL**: `/ocr/getAll`
- **Method**: `POST`
- **Description**: Extracts all key details and table data from an invoice image.
- **Request**:
    - A POST request with a file parameter named `image` containing the invoice image.
- **Response**:
    ```json
    {
        "vendorName": "Vendor Name",
        "invoiceNumber": "12345",
        "invoiceDate": "2025-04-01",
        "dueDate": "2025-04-10",
        "poNumber": "PO6789",
        "table": {
            "items": [
                {"item": "Product A", "price": 100, "quantity": 2},
                {"item": "Product B", "price": 50, "quantity": 3}
            ]
        }
    }
    ```

#### Example Usage with `curl`
```bash
curl -X POST -F "image=@/path/to/invoice.png" http://localhost:5000/ocr/getAll
