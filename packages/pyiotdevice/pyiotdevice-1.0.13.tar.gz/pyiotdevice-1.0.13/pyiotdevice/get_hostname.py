def get_hostname(apn):
    """Convert APN to hostname by extracting and reversing the hex part."""
    return (f"{apn.split(':')[0]}{''.join([apn.split(':')[1][i:i+2] for i in range(0, 6, 2)][::-1])}" 
            if ':' in apn and len(apn.split(':')[1]) >= 6 else None)