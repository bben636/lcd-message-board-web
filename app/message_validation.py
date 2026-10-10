def parse_text_update(data: object) -> tuple[int, str]:
    """validation of decoded message"""
    
    #web socket can send list, number or null instead of object.
    if not isinstance(data, dict):
        raise ValueError("message must be JSON")
    
    sequence = data.get("seq")
    text = data.get("text")
    
    #Reject string float or boolean as seq number
    if type (sequence) is not int or sequence < 1:
        raise ValueError ("seq must be a positive int")
    
    if not isinstance(text, str):
        raise ValueError ("text  must be string type")
    
    return sequence, text

