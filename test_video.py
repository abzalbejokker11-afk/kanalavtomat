import asyncio
import video_maker

async def test():
    print("Testing video generation...")
    file_path = await video_maker.create_video("Salom, bu test video! Dopingga qarshi kurashamiz.")
    if file_path:
        print(f"Video created at: {file_path}")
    else:
        print("Failed to create video")

if __name__ == "__main__":
    asyncio.run(test())
