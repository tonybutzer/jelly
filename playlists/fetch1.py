import requests

JELLYFIN_URL = "http://viki:8096"
API_KEY = "cd2d7cb0952b493188dbcaf96c0617e0"
USER_ID = "10225601335f436194b90eaa38f069a7"

headers = {
    "Authorization": f'MediaBrowser Token="{API_KEY}"',
    "Content-Type": "application/json"
}

def export_playlist_to_m3u(playlist_name="1", output_filename="playlist_1.m3u"):
    # 1. Find the playlist ID by listing user playlists
    playlists_url = f"{JELLYFIN_URL}/Users/{USER_ID}/Items"
    params = {
        "IncludeItemTypes": "Playlist",
        "Recursive": "true"
    }
    response = requests.get(playlists_url, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f"Error fetching items: {response.status_code} - {response.text}")
        return
        
    playlists = response.json().get("Items", [])
    playlist_id = None
    
    for p in playlists:
        if p.get("Name") == playlist_name:
            playlist_id = p.get("Id")
            break
            
    if not playlist_id:
        print(f"Playlist named '{playlist_name}' could not be found.")
        return

    # 2. Fetch the items inside the specific playlist
    items_url = f"{JELLYFIN_URL}/Playlists/{playlist_id}/Items"
    item_params = {
        "UserId": USER_ID,
        "Fields": "Path,MediaSources"  # <--- This forces Jellyfin to populate the Path field
    }
    #items_url = f"{JELLYFIN_URL}/Playlists/{playlist_id}/Items"
    #item_params = {"UserId": USER_ID}
    items_response = requests.get(items_url, headers=headers, params=item_params)
    
    if items_response.status_code != 200:
        print(f"Error fetching playlist items: {items_response.status_code}")
        return
        
    items = items_response.json().get("Items", [])

    # 3. Format as M3U text content
    m3u_lines = ["#EXTM3U"]
    for item in items:
        title = item.get("Name", "Unknown")
        # Jellyfin runtime is in ticks (1 second = 10,000,000 ticks)
        duration_seconds = item.get("RunTimeTicks", 0) // 10000000
        path = item.get("Path", "")
        
        m3u_lines.append(f"#EXTINF:{duration_seconds},{title}")
        m3u_lines.append(path)

    # 4. Save to local .m3u file
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write("\n".join(m3u_lines))
        
    print(f"Successfully exported playlist '{playlist_name}' ({len(items)} items) to {output_filename}")

if __name__ == "__main__":
    export_playlist_to_m3u("1", "playlist_1.m3u")
