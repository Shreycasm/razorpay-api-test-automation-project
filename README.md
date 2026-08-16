# Razorpay API Automation Framework

A scalable API automation framework built with **Python and Pytest** for testing Razorpay APIs.

This project is being developed from the ground up with a focus on **clean architecture, reusable components, API validation, negative testing, structured logging, reporting, and CI/CD**.

The goal is to build more than a collection of API test scripts — the goal is to understand how a maintainable API automation framework is designed.

---

## 🎯 Project Goals

This project aims to demonstrate:

* API automation using Python and Pytest
* Reusable API client design
* Request and response validation
* Positive and negative API testing
* API contract validation
* Test data management
* Environment-based configuration
* Structured logging
* Test reporting
* Parallel test execution
* CI/CD integration
* Maintainable and scalable test architecture

---

## 🛠️ Tech Stack

| Technology     | Purpose                                   |
| -------------- | ----------------------------------------- |
| Python         | Programming language                      |
| Pytest         | Test framework                            |
| Requests       | HTTP client                               |
| Pydantic       | Request/response validation               |
| JSON Schema    | API contract validation                   |
| Structlog      | Structured logging                        |
| Faker          | Test data generation                      |
| Allure         | Test reporting                            |
| GitHub Actions | CI/CD                                     |
| uv             | Python package and environment management |

---

## 🏗️ Planned Architecture

The framework will be developed using separate layers for API communication, models, configuration, utilities, and tests.

```text
                    Test Layer
                        │
                        ▼
                API Service Layer
                        │
                        ▼
                 Base API Client
                        │
                        ▼
                 Requests Library
                        │
                        ▼
                       HTTP
                        │
                        ▼
                 Razorpay Sandbox
```

Supporting components:

```text
Configuration
Request / Response Models
Test Data
Schema Validation
Logging
Reporting
CI/CD
```

This separation is intended to keep API communication independent from test logic and make the framework easier to extend.

---

## 📌 Initial Scope

The first API being automated is the **Razorpay Orders API**.

Planned operations include:

The initial focus is on building the framework around the Orders API. Additional APIs may be introduced as the project evolves.

---

## 🧪 Testing Strategy

The test suite will cover multiple types of API scenarios.

### Positive Testing

Valid requests will be used to verify expected API behavior.

Examples:

* Create an order with valid data
* Fetch an existing order
* List orders
* Update supported order fields

### Negative Testing

Invalid inputs will be deliberately sent to verify API validation.

Examples:

* Missing required fields
* Invalid data types
* Invalid amounts
* Unsupported currencies
* Empty values
* Boundary values
* Invalid request payloads

### Contract Testing

API responses will be validated against expected structures using JSON Schema.

---

## 🔍 Validation Strategy

The framework will use multiple levels of validation instead of relying only on HTTP status codes.

```text
HTTP Status Code
       ↓
Response Structure
       ↓
Pydantic Validation
       ↓
JSON Schema Validation
       ↓
Business Assertions
```

This approach helps identify issues where an API returns a successful HTTP response but the response itself does not match the expected contract.

---

## 🔐 Configuration & Security

API credentials and environment-specific configuration will not be hard-coded into the source code.

Environment variables will be used for sensitive configuration such as:

```text
RAZORPAY_BASE_URL
RAZORPAY_KEY_ID
RAZORPAY_KEY_SECRET
```

Sensitive files such as `.env` will be excluded from version control.

---

## 🚧 Current Status

**Project initialized — active development**

Current status:

* [x] Initialize Python project with `uv`
* [x] Implement configuration management
* [x] Implement structured logging
* [x] Implement Base API Client
* [x] Add request and response models
* [x] Add API error handling

---

## 💡 Why This Project?

The purpose of this project is to practice designing an API automation framework from the ground up.

Rather than focusing only on writing individual test cases, the project focuses on understanding:

* How reusable automation components are designed
* How test code should be separated from API implementation
* How API contracts can be validated
* How negative testing can identify API weaknesses
* How automation can be integrated into CI/CD
* How an automation framework can scale as the number of APIs and tests increases

---

## 📚 Project Status

This repository is **actively developed** and will evolve as new framework capabilities are implemented.

Each major feature is developed incrementally and tracked through Git commits.
