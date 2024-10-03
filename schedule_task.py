from app import capture_facebook_pages, capture_youtube_channels, capture_instagram_profiles, capture_twitter_profiles


def run_auto_capture():
    print("Starting scheduled social media data capture...")

    # Call the functions to capture social media data
    print("Capturing Facebook data...")
    capture_facebook_pages()

    print("Capturing YouTube data...")
    capture_youtube_channels()

    print("Capturing Instagram data...")
    capture_instagram_profiles()

    print("Capturing Twitter data...")
    capture_twitter_profiles()

    print("All data capture complete.")


if __name__ == '__main__':
    run_auto_capture()
