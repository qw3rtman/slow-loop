# slow-loop

Perception-planning-control loop used for some real-world experiments on a reverse-engineered [DJI RoboMaster S1](https://www.dji.com/robomaster-s1). Built for slow perception/planning (e.g., pipelines with deep vision models on a laptop CPU).

## why
We reverse-engineered a [DJI RoboMaster S1](https://www.dji.com/robomaster-s1) as a cheap ($500) test-bed for evaluating deep visuomotor policies in the real-world. This was a follow-up to our previous work, *[Domain Adaptation Through Task Distillation](https://arxiv.org/abs/2008.11911) (ECCV 2020)*. We wrote a wrapper that allowed us to receive a video stream and send control commands over UDP. To go mobile, we would either need to 1) send a live feed over a mobile hotspot to a machine with a GPU, or 2) somehow manage a perception-planning-control loop with only a laptop CPU (slow inference time). We chose the second option. Our video feed was 30 fps and our perception alone ranged from 40ms - 160ms on a CPU, so this would prove tricky.

I built a controller that could concurrently perform inference and control, schedule or batch inference on queued video frames to not fall too far behind, and record all frames and control for replay.
