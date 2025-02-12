## API Documentation

## Overview

This API provides endpoints for executing different types model views description and (partially) model transformations based on view definitions and transformations. The API uses Flask and expects JSON payloads for all requests.

## Base URL

```
http://<host>:5000
```

## Endpoints

### 1. **Select View**

**Endpoint:**

```
POST /select
```

**Description:** Based on the given information, it generates the elements that should be filtered in in a model view description. Considering the VPDL context, it generates the SELECT part as a JSON containing all elements to be selected per meta-class.

**Request Body:**

```json
{
  "view_name": "string",
  "prompt_type": "string",
  "view_description": "string",
  "relations": "string"
}
```

**Important**: The "relations" parameter should follow exactly the format output of the JOIN output.

**Response:**

```json
{
  "result": "string"
}
```

**Error Responses:**

- `400 Bad Request` if required fields are missing or `view_name` is incorrect.

---

### 2. **Where View**

**Endpoint:**

```
POST /where
```

**Description:** Based on the given information, it generates the natural language explanations that can be used by the user to comput the established virtual relations. Considering the VPDL context, it generates the WHERW part as a JSON containing all one explanation per virtual realtion sent in the "relations" input.

**Request Body:**

```json
{
  "view_name": "string",
  "prompt_type": "string",
  "view_description": "string",
  "relations": "string"
}
```

**Important**: The "relations" parameter should follow exactly the format output of the JOIN output.

**Response:**

```json
{
  "result": "string"
}
```

**Error Responses:**

- `400 Bad Request` if required fields are missing or `view_name` is incorrect.

---

### 3. **Join View**

**Endpoint:**

```
POST /join
```

**Description:** Based on the given information, it generates the potential virtual relations between the 2 given metamodels. Considering the VPDL context, it generates the JOIN part as a JSON containing all meta-classes pairs that should be included in the final VPDL code.

**Request Body:**

```json
{
  "view_name": "string",
  "prompt_type": "string",
  "view_description": "string"
}
```

**Response:**

```json
{
  "result": "string"
}
```

**Error Responses:**

- `400 Bad Request` if required fields are missing or `view_name` is incorrect.

---

### 4. **VPDL View**

**Endpoint:**

```
POST /vpdl
```

**Description:** Executes a VPDL operation. Essentially, it executes in sequence the JOIN->SELECT->WHERE operations together with a final code generation that creates the draft of the VPDL to be used into EMF Views.

**Request Body:**

```json
{
  "view_name": "string",
  "prompt_type": "string",
  "view_description": "string"
}
```

**Response:**

```json
{
  "result": "string"
}
```

**Error Responses:**

- `400 Bad Request` if required fields are missing or `view_name` is incorrect.

---

### 5. **ATL Transformation**

**Endpoint:**

```
POST /atl
```

**Description:** Create an list of classes pairs (equivalent to the JOIN operation) that can help the users in ATL development.

**Request Body:**

```json
{
  "transformation_name": "string",
  "prompt_type": "string",
  "transformation_description": "string"
}
```

**Response:**

```json
{
  "result": "string"
}
```

**Error Responses:**

- `400 Bad Request` if required fields are missing or `transformation_name` is incorrect.

---

## Error Handling

- All endpoints return `400 Bad Request` when required fields are missing or incorrect values are provided.
- Responses include an `error` field with a descriptive message.
