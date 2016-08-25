**This documentation is automatically generated.**

**Output schemas only represent `data` and not the full output; see output examples and the JSend specification.**

# /api/helloworld/?

    Content-Type: application/json

## GET


**Input Schema**
```json
null
```



**Output Schema**
```json
{
    "type": "string"
}
```





<br>
<br>

# /api/post/?

    Content-Type: application/json

## POST


**Input Schema**
```json
{
    "properties": {
        "body": {
            "type": "string"
        },
        "index": {
            "type": "number"
        },
        "title": {
            "type": "string"
        }
    },
    "required": [
        "title",
        "body"
    ],
    "type": "object"
}
```



**Output Schema**
```json
{
    "properties": {
        "message": {
            "type": "string"
        }
    },
    "type": "object"
}
```





<br>
<br>

# /api/urlparam/\(?P\<fname\>\[a\-zA\-Z0\-9\_\\\-\]\+\)/\(?P\<lname\>\[a\-zA\-Z0\-9\_\\\-\]\+\)/?$

    Content-Type: application/json

## GET


**Input Schema**
```json
null
```



**Output Schema**
```json
{
    "type": "string"
}
```





<br>
<br>

# /api/user/\(?P\<id\>\[0\-9\]\+\)/group

    Content-Type: application/json

## GET


**Input Schema**
```json
null
```



**Output Schema**
```json
{
    "properties": {
        "gtype": {
            "type": "string"
        },
        "id": {
            "type": "number"
        }
    },
    "type": "object"
}
```




