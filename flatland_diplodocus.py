#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot    as plt
import matplotlib.patches   as patches
import matplotlib.animation as animation
import sys
import random


paused = False
def on_press(event):
    global paused

    sys.stdout.flush()

    if event.key == 'enter':
        if paused: ani.event_source.start()
        else:      ani.event_source.stop()
        paused ^= True

    elif event.key == 'up':
        position = ax.patches[-1].get_y()
        ax.patches[-1].set_y(position + 1)

    elif event.key == 'shift+up':
        position = ax.patches[-1].get_y()
        ax.patches[-1].set_y(position + 5)

    elif event.key == 'down':
        position = ax.patches[-1].get_y()
        if position:
            ax.patches[-1].set_y(position - 1)

    elif event.key == 'shift+down':
        position = ax.patches[-1].get_y()
        if position>4:
            ax.patches[-1].set_y(position - 5)



def epoch(birthday, delta, edge):
    get_height = lambda idx:      ax.patches[idx].get_height()
    set_height = lambda idx, val: ax.patches[idx].set_height(val)
    get_y =      lambda idx:      ax.patches[idx].get_y()
    set_y =      lambda idx, val: ax.patches[idx].set_y(val)
    set_parent = lambda idx:      ax.patches[idx].set_fc('gray')
    set_child  = lambda idx:      ax.patches[idx].set_fc('blue')
    is_child   = lambda idx:      ax.patches[idx]._original_facecolor == 'blue'

    tree_idx = -1
    diplodocus_count = len(ax.patches[:-1])
    diplodocus_index_range = range(0, diplodocus_count)


    def alive(height):
        bottom = get_y(tree_idx)
        top    = bottom + get_height(tree_idx)
        return bottom <= height <= top


    def next_generation(height):
        height += random.randint(-delta, delta)
        return height if height>0 else 0


    def animate(frame_number):
        time_to_kill = lambda idx: (abs(birthday[idx] - frame_number) >= edge)

        # Growing up
        [set_parent(i) for i in diplodocus_index_range]

        # Evaluate
        for idx in diplodocus_index_range:
            height = get_height(idx)

            # Hide dead's
            if not alive(height):
                set_height(idx, 0)
                continue

            # Skip last step childs
            if is_child(idx):
                continue

            # Kill old parents
            if time_to_kill(idx):
                set_height(idx, 0)
                continue

            # Create child
            for i in [idx-1, idx+1]:
                if i in diplodocus_index_range and not alive(get_height(i)):
                    set_height(i, next_generation(height))
                    set_child(i)
                    birthday[i] = frame_number



        return ax.patches

    return animate



if __name__ == "__main__":
    pause = False
    count=100
    high_bound=30
    delta=2
    edge=3
    base_length=15
    tree_bound=10
    tree_height=10

    random.seed(12345678)

    HIST_BINS = range(0,count)

    fig, ax = plt.subplots()
    

    # ax.grid()
    ax.set_xlim(0, len(HIST_BINS)-1)
    ax.set_ylim(0, high_bound * 2)
    # ax.set_ylabel('Высота')
    # ax.set_xlabel('Диплодоки')

    # Create dino
    birthday=[]
    for index, height in enumerate([random.randrange(base_length) for i in HIST_BINS]):
        diplodocus = patches.Rectangle((index,0), 1, height, ec='black', fc='gray')
        ax.add_patch(diplodocus)
        birthday.append(0)
        
    # Create tree
    tree = patches.Rectangle((0,tree_height), len(HIST_BINS), tree_bound, ec='black', fc='green', alpha=0.5)
    ax.add_patch(tree)

    # Start the world
    ani = animation.FuncAnimation(fig, epoch(birthday, delta, edge),
                                  100, interval=100, repeat=False, blit=True)

    # # Save gif
    # ani.save('demo.gif', writer='imagemagick', fps=30)
    
    # # Save video
    # with open("demo.html", "w") as fd:
    #     print(ani.to_html5_video(), file=fd)

    # Realtime show
    fig.canvas.mpl_connect('key_press_event', on_press)
    plt.show()
