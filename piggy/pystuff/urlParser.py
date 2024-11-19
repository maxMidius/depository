from urllib.parse import urlsplit

def get_base_url(url):
  """
  This function extracts the base URL from a given URL string.

  Args:
      url: The URL string to extract the base URL from.

  Returns:
      The base URL (scheme, netloc) of the provided URL.
  """
  parsed_url = urlsplit(url)
  base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
  return base_url

# Example usage
url = "http://some.host.com:8080/app1/param"
base_url = get_base_url(url)
print(base_url)  # Output: http://some.host.com:8080
