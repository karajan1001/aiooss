"""
A simple async example to use aiooss
"""
import asyncio
import os

from aiooss import AioBucket, AioObjectIterator, Auth

OSS_ACCESS_KEY_ID = os.environ.get("OSS_ACCESS_KEY_ID")
OSS_SECRET_ACCESS_KEY = os.environ.get("OSS_SECRET_ACCESS_KEY")
BUCKET_NAME = os.environ.get("OSS_TEST_BUCKET_NAME")


async def async_go():
    """
    example coroutine
    """
    obj_name = "your_obj"
    folder = "readme"
    data_obj = f"{folder}/{obj_name}"

    auth = Auth(OSS_ACCESS_KEY_ID, OSS_SECRET_ACCESS_KEY)
    async with AioBucket(
        auth, "http://oss-cn-hangzhou.aliyuncs.com", BUCKET_NAME
    ) as bucket:

        # upload object to oss
        data = b"\x01" * 1024
        resp = await bucket.put_object(data_obj, data)

        # upload object to oss
        resp = await bucket.get_object(data_obj)
        obj_read = await resp.read()
        assert obj_read == data

        # list oss objects
        print(f"objects in {folder}")
        async for obj in AioObjectIterator(
            bucket, prefix=folder
        ):  # pylint: disable=not-an-iterable
            print(obj.key)

        # delete object
        resp = await bucket.delete_object(data_obj)
        print(f"objects in {folder}, after delete")
        async for obj in AioObjectIterator(
            bucket, prefix=folder
        ):  # pylint: disable=not-an-iterable
            print(obj.key)


asyncio.run(async_go())
