# Booking Management API with Web Dashboard

This project represents a REST API developed in Python using Flask, designed for managing room bookings. Additionally, it offers a minimalist web interface (`dashboard.html`) for intuitively viewing, filtering, and managing reservations.

---

## 🔧 Core API Features

### Authentication
- **Endpoint:** `/login`  
- **Method:** `POST`  
- **Description:** Accepts a username and password. If the credentials are correct (`admin` / `1234`), it returns a JWT token which must be included in the `Authorization` header for protected operations.  
- **Request Body:**
```json
{
  "username": "admin",
  "password": "1234"
}
```

### Add Booking (requires token)
- **Endpoint:** `/bookings`  
- **Method:** `POST`  
- **Required Header:** `Authorization: Bearer <token>`  
- **Request Body:**
```json
{
  "name": "Ion Popescu",
  "room": "A1",
  "date": "2025-06-10"
}
```

### List Bookings (no authentication)
- **Endpoint:** `/bookings`  
- **Method:** `GET`  
- **Optional filters:** `?name=...&room=...&date=...`

### Delete Booking (requires token)
- **Endpoint:** `/bookings/<booking_id>`  
- **Method:** `DELETE`  
- **Required Header:** `Authorization: Bearer <token>`

---

## 🔄 XML Export and Validation

The application includes support for exporting bookings to XML format and validating them using an XSD schema file.

### XML Export
- **Function:** `bookings_to_xml(bookings)`  
- **Generated File:** `bookings.xml`  
- **Description:** Generates an XML file with all current bookings. Also available via:  
  - **Endpoint:** `GET /bookings/xml`  
  - **Returns:** XML content with `Content-Type: application/xml`

### XML Validation
- **Function:** `validate_xml(xml_path="bookings.xml", xsd_path="schema.xsd")`  
- **Schema File:** `schema.xsd` (user-defined)  
- **Description:** Checks if `bookings.xml` conforms to the structure defined in the XSD.  
  - **Endpoint:** `GET /bookings/validate`  
  - **Returns:** JSON with `valid: true/false` and a validation message

These functionalities are also integrated into the HTML dashboard via accessible buttons in the interface.

---

## 🖥️ Web Interface: Dashboard

- **Endpoint:** `/dashboard`  
- **Methods:** `GET`, `POST`  
- **Description:** Provides a simple HTML form and table interface for:
  - Viewing current bookings
  - Filtering by `name`, `room`, `date`
  - Adding new bookings via form (no authentication required)
  - Deleting bookings from UI (no authentication required)
  - Exporting to XML and validating XML directly from the UI

### Important Note
> The HTML interface does NOT use authentication mechanisms (JWT tokens). It is assumed to be used within an internal network by implicitly authorized users. For complete security, it is recommended to protect this route with additional methods (e.g., server-level authentication, HTTP Basic Auth, etc.).

---

## 💾 Persistence

- All bookings are saved in the `data.json` file.
- Data is automatically loaded and saved on every modification.

---

## 🚀 Running the Application

```bash
python main.py
```

Upon startup, the app will automatically open the browser at:  
`http://127.0.0.1:5000/dashboard`

---

## 📦 Dependencies

- `requirements.txt`

To install:
```bash
pip install -r requirements.txt
```

---

## 📫 API Testing Examples (Postman)

1. Login (`/login`) → copy token (POST)  
2. Create booking with `Authorization: Bearer <token>` (POST)  
3. Filter bookings (GET)  
4. Delete booking by ID (DELETE)  
5. Export to XML and validate (GET)

---

## 📁 File Structure

```
├── main.py               # Main application logic
├── utils.py              # Functions for XML conversion and validation
├── data.json             # Booking persistence
├── bookings.xml          # XML representation of bookings
├── schema.xsd            # XSD schema for XML validation
├── templates/
│   ├── dashboard.html    # HTML interface
```

---

## ⚠️ Final Note

This project is designed for educational or internal prototyping purposes. It is not recommended for production use without additional security measures.
