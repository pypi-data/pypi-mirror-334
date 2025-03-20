import asyncio
import json
import sys

from isubrip.scrapers.scraper import ScraperFactory


async def save_mock_data(url: str) -> None:
    """Save mock data for testing from a given iTunes URL."""
    # Initialize scraper
    scraper = ScraperFactory.get_scraper_instance(url=url)
    
    # Get media data
    response = await scraper.get_data(url=url)
    
    # Save API response
    api_response_path = output_dir / "api_response.json"
    api_response_path.write_text(json.dumps(response.dict(), indent=2))

    # Get playlist and subtitles data
    media_data = response.media_data[0]  # Get first media item
    if media_data.playlist:
        playlist = await scraper.load_playlist(url=media_data.playlist)
        
        # Save playlist data
        playlist_path = output_dir / "playlist.m3u8"
        playlist_path.write_text(playlist)
        
        # Download and save subtitles
        matching_subtitles = scraper.find_matching_subtitles(
            main_playlist=playlist,
            language_filter=None,
        )
        
        for i, sub in enumerate(matching_subtitles):
            subtitles_data = await scraper.download_subtitles(
                media_data=sub,
                subrip_conversion=False,
            )
            
            sub_path = output_dir / f"subtitles_{i}.vtt"
            sub_path.write_bytes(subtitles_data.content)

async def main():
    # Example URL and output directory
    if len(sys.argv) >= 2:
        for url in sys.argv[1:]:
            await save_mock_data(url)

    else:
        print("Usage: python generate_itunes_subtitles_mock_data.py <url> [<url> ...]")
        exit(1)

if __name__ == "__main__":
    asyncio.run(main())
