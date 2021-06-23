import asyncio


async def foo():
    print('running in foo()')
    await asyncio.sleep(2)
    print('end foo')


async def bar():
    print('running in bar')
    await asyncio.sleep(5)
    print('end bar')


async def bar2():
    print('running in bar2')
    await asyncio.sleep(3)
    print('end bar2')


ioloop = asyncio.get_event_loop()
tasks = [ioloop.create_task((foo())), ioloop.create_task(bar()), ioloop.create_task(bar2())]
wait_tasks = asyncio.wait(tasks)
ioloop.run_until_complete(wait_tasks)
ioloop.close()
