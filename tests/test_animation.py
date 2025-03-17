import pytest
from animation import Animation


@pytest.fixture
def frames():
    return ["frame1", "frame2", "frame3"]


@pytest.fixture
def animation(frames):
    return Animation(frames=frames, speed=2, loop=True)


@pytest.fixture
def non_looping_animation(frames):
    return Animation(frames=frames, speed=2, loop=False)


def test_init(animation, frames):
    assert animation.frames == frames
    assert animation.current_frame == 0
    assert animation.speed == 2
    assert animation.loop is True
    assert animation.is_finished is False


def test_update(animation):
    assert animation.update(0.4) == "frame1"
    assert animation.update(0.2) == "frame2"
    assert animation.update(0.5) == "frame3"  # ще один перехід
    assert animation.update(0.5) == "frame1"


def test_update_no_loop(non_looping_animation):
    assert non_looping_animation.update(0.4) == "frame1"
    assert non_looping_animation.update(0.2) == "frame2"
    assert non_looping_animation.update(0.5) == "frame3"  # Останній кадр
    assert non_looping_animation.update(0.5) == "frame3"  # Далі не змінюється (is_finished=True)


def test_reset(animation):
    animation.update(1.0)
    animation.reset()
    assert animation.current_frame == 0
    assert animation.is_finished is False
