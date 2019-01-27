---
layout: post
title: "Understanding the Game Loop of Cocos2d-x"
date: 2019-01-24 17:21:10 +0800
category: Code-Review
tags: cocos2dx game-engine
---

This post is a code review of the game loop of [Cocos2d-x (v3.10)](https://github.com/cocos2d/cocos2d-x/tree/v3). The game loop is the heart of a game. It keeps the game running.

In the game loop of Cocos2d-x, there are two phases: 1. Drawing the current scene; 2. Cleaning up objects in the auto-release pool. In the `DisplayLinkDirector::mainLoop()`:

```c++
drawScene();
PoolManager::getInstance()->getCurrentPool()->clear();
```

What jobs done in the [`drawScene`](https://github.com/cocos2d/cocos2d-x/blob/e71ef8218cb58a66ec07cf9cc5ac80ac4e695ebd/cocos/base/CCDirector.cpp#L259) method?

- Handle input events.

    ```c++
    if (_openGLView)
    {
        _openGLView->pollEvents();
    }
    ```

    However, the `pollEvents` of `GLView` is an empty implementation. I have find only one actual implementation which calls the [`glfwPollEvents`](https://www.glfw.org/docs/latest/group__window.html#ga37bd57223967b4211d60ca1a0bf3c832) method in the `CCGLViewImpl-desktop` file. 

- Tick the scheduler.

    ```c++
    if (! _paused)
    {
        _eventDispatcher->dispatchEvent(_eventBeforeUpdate);
        _scheduler->update(_deltaTime);
        _eventDispatcher->dispatchEvent(_eventAfterUpdate);
    }
    ```

- Clear GL buffers and all [FBOs](https://www.khronos.org/opengl/wiki/Framebuffer_Object).

    ```c++
    _renderer->clear();
    experimental::FrameBuffer::clearAllFBOs();
    ```

- Set the next scene, i.e. if the `_nextScene` is not null, assign it to the `_runningScene`.

    ```c++
    if (_nextScene)
    {
        setNextScene();
    }
    ```

    This code fragment prompts that if we write a statement to switch scene, it will take effect only in the next frame.

- Push matrix.

    ```c++
    pushMatrix(MATRIX_STACK_TYPE::MATRIX_STACK_MODELVIEW);
    ```

    ???

- Update the physics world if there is.

    ```c++
    #if (CC_USE_PHYSICS || (CC_USE_3D_PHYSICS && CC_ENABLE_BULLET_INTEGRATION) || CC_USE_NAVMESH)
        _runningScene->stepPhysicsAndNavigation(_deltaTime);
    #endif
    ```

- Render the scene (the actual work of "draw scene").

    ```c++
    _renderer->clearDrawStats();
    _runningScene->render(_renderer);
    ```

- If there is a notification node, draw it.

    ```c++
    if (_notificationNode)
    {
        _notificationNode->visit(_renderer, Mat4::IDENTITY, 0);
    }
    _renderer->render();
    ```

- Pop matrix.

    ```c++
    popMatrix(MATRIX_STACK_TYPE::MATRIX_STACK_MODELVIEW);
    ```

    ???

- Swap buffers

    ```c++
    if (_openGLView)
    {
        _openGLView->swapBuffers();
    }
    ```

