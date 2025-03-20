import json
import os

from mcp.server.fastmcp import FastMCP
from requests_oauthlib import OAuth1Session


# Initialize FastMCP server
mcp = FastMCP(
    "DevHub CMS MCP",
    description="Integration with DevHub CMS to manage content")

devhub_api = OAuth1Session(
    os.environ['DEVHUB_API_KEY'],
    client_secret=os.environ['DEVHUB_API_SECRET'])
base_url = '{}/api/v2/'.format(os.environ['DEVHUB_BASE_URL'])


@mcp.tool()
def get_hours_of_operation(location_id: int, hours_type: str = 'primary') -> list:
    """Get the hours of operation for a DevHub location

    Returns a list of items representing days of the week

    Except for the special case formatting, this object is a list of 7 items which represent each day.

    Each day can can have one-four time ranges. For example, two time ranges denotes a "lunch-break". No time ranges denotes closed.

    Examples:
    9am-5pm [["09:00:00", "17:00:00"]]
    9am-12pm and 1pm-5pm [["09:00:00", "12:00:00"], ["13:00:00", "17:00:00"]]
    Closed - an empty list []

    Args:
        location_id: DevHub Location ID
        hours_type: Defaults to 'primary' unless the user specifies a different type
    """
    r = devhub_api.get('{}locations/{}'.format(base_url, location_id))
    content = json.loads(r.content)
    return content['hours_by_type'].get(hours_type, [])


@mcp.tool()
def update_hours(location_id: int, new_hours: list, hours_type: str = 'primary') -> str:
    """Update the hours of operation for a DevHub location

    Send a list of items representing days of the week

    Except for the special case formatting, this object is a list of 7 items which represent each day.

    Each day can can have one-four time ranges. For example, two time ranges denotes a "lunch-break". No time ranges denotes closed.

    Examples:
    9am-5pm [["09:00:00", "17:00:00"]]
    9am-12pm and 1pm-5pm [["09:00:00", "12:00:00"], ["13:00:00", "17:00:00"]]
    Closed - an empty list []

    Args:
        location_id: DevHub Location ID
        new_hours: Structured format of the new hours
        hours_type: Defaults to 'primary' unless the user specifies a different type
    """
    r = devhub_api.put(
        '{}locations/{}/'.format(base_url, location_id),
        json={
            'hours': [
                {
                    'type': hours_type,
                    'hours': new_hours,
                }
            ]
        },
    )
    content = json.loads(r.content)
    return 'Updated successfully'


@mcp.tool()
def upload_image(base64_image_content: str, filename: str) -> str:
    """Upload an image to the DevHub media gallery

    Supports webp, jpeg and png images

    Args:
        base64_image_content: Base 64 encoded content of the image file
        filename: Filename including the extension
    """
    payload = {
        'type': 'image',
        'upload': {
            'file': base64_image_content,
            'filename': filename,
        }
    }
    r = devhub_api.post(
        '{}images/'.format(base_url),
        json=payload,
    )
    image = r.json()
    return f"""
Image ID: {image['id']}
Image Path (for use in HTML src attributes): {image['absolute_path']}
"""


@mcp.tool()
def get_blog_post(post_id: int) -> str:
    """Get a single blog post

    Args:
        post_id: Blog post id
    """
    r = devhub_api.get('{}posts/{}/'.format(base_url, post_id))
    post = r.json()
    return f"""
Post ID: {post['id']}
Title: {post['title']}
Date: {post['date']}

Content (HTML):
{post['content']}
"""


@mcp.tool()
def create_blog_post(site_id: int, title: str, content: str) -> str:
    """Create a new blog post

    Args:
        site_id: Website ID where the post will be published. Prompt the user for this ID.
        title: Blog post title
        content: HTML content of blog post. Should not include a <h1> tag, only h2+
    """
    payload = {}
    payload['site_id'] = site_id
    payload['content'] = content
    payload['title'] = title
    r = devhub_api.post(
        '{}posts/'.format(base_url),
        json=payload,
    )
    post = r.json()
    return f"""
Post ID: {post['id']}
Title: {post['title']}
Date: {post['date']}

Content (HTML):
{post['content']}
"""


@mcp.tool()
def update_blog_post(post_id: int, title: str = None, content: str = None) -> str:
    """Update a single blog post

    Args:
        post_id: Blog post ID
        title: Blog post title
        content: HTML content of blog post. Should not include a <h1> tag, only h2+
    """
    payload = {}
    if content:
        payload['content'] = content
    if title:
        payload['title'] = title
    r = devhub_api.put(
        '{}posts/{}/'.format(base_url, post_id),
        json=payload,
    )
    post = r.json()
    return f"""
Post ID: {post['id']}
Title: {post['title']}
Date: {post['date']}

Content (HTML):
{post['content']}
"""


@mcp.tool()
def get_nearest_location(business_id: int, latitude: float, longitude: float) -> str:
    """Get the nearest DevHub location

    Args:
        business_id: DevHub Business ID associated with the location. Prompt the user for this ID
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    r = devhub_api.get('{}locations/'.format(base_url), params={
        'business_id': business_id,
        'near_lat': latitude,
        'near_lon': longitude,
    })
    objects = json.loads(r.content)['objects']
    if objects:
        return f"""
Location ID: {objects[0]['id']}
Location name: {objects[0]['location_name']}
Location url: {objects[0]['location_url']}
Street: {objects[0]['street']}
City: {objects[0]['city']}
State: {objects[0]['state']}
Country: {objects[0]['country']}
"""


def main():
    """Run the MCP server"""
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
