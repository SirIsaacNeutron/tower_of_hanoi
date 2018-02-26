'''
The Tower of Hanoi is an old puzzle in which the player must try to get
all disks from the first tower (the leftmost one) to the last tower
(the rightmost one). The disks have different sizes; only the topmost
disk can be moved from a tower, and disks must always be smaller than
the disks under them. And when the player moves disks, the disks always
go as far down the Tower as possible.

You can read more about the Tower of Hanoi puzzle here:
https://en.wikipedia.org/wiki/Tower_of_Hanoi

Created on Feb 15, 2018.

@author SirIsaacNeutron
'''

EMPTY = 0  # Represents an empty space in a Tower


class NoDisksError(Exception):
    """Raised when there are no Disks in a Tower, and the player
    tries to move a Disk from that Tower to another.
    """
    pass


class InvalidMoveError(Exception):
    """Raised when the player tries to move a Disk to a Tower whose
    bottommost Disk is smaller than it.
    """
    pass


class InvalidFirstMoveError(Exception):
    """Raised when the player does not make his first move from
    Tower 1.
    """
    pass


class Game:
    """Represents a session of Tower of Hanoi. There are 3 Towers in
    the game; at the beginning, the first Tower is full of Disks, and
    the other 2 Towers are empty.
    """
    def __init__(self, num_disks_per_tower: int):
        self.tower_one = Tower(num_disks_per_tower)
        self.tower_two = Tower(num_disks_per_tower, empty=True)
        self.tower_three = Tower(num_disks_per_tower, empty=True)
        
        self.min_moves_required = 2**num_disks_per_tower - 1
        self.num_moves_made = 0
        
    def is_over(self) -> bool:
        """Return True if self.tower_three is totally full of Disks."""
        return all(disk != EMPTY for disk in self.tower_three)
    
    def print_towers(self) -> None:
        """Print all three Towers side by side."""
        print(' 1   2   3')
        towers = [self.tower_one, self.tower_two, self.tower_three]
        
        disk_index = 0
        # Print the first element of every tower's .disks list
        # Print the second element of every tower's .disks list
        # etc.
        while disk_index < len(towers[0].disks):
            for tower in towers:
                if tower[disk_index] == EMPTY:
                    print('[ ]', end=' ')
                else:
                    print('[' + str(tower[disk_index].size) + ']', end=' ')
            disk_index += 1
            print()


class Disk:
    """A disk in the puzzle. Disks have a size represented by an
    integer; the smaller the integer, the smaller the Disk is. Disks
    are contained in Towers and to win the game, the final Tower
    must be totally filled with Disks.
    """
    def __init__(self, size: int):
        self.size = size
        
    def is_smaller_than(self, other_disk) -> bool:
        """Return True if this Disk is smaller than other_disk."""
        return self.size < other_disk.size
    
    def __repr__(self):
        return 'Disk(' + str(self.size) + ')'


class Tower:
    """A tower, or pole, in the Tower of Hanoi puzzle. A Tower can have
    an arbitrary number of disks, and the player can pick a disk and move
    it to another Tower. There are only 3 Towers in the puzzle.
    """
    def __init__(self, num_disks: int, empty=False):
        if not empty:
            self.disks = [Disk(num) for num in range(1, num_disks + 1)]
        else:
            # self.disks has to be of length num_disks, regardless
            # of whether it has disks or not.
            self.disks = [EMPTY for num in range(0, num_disks)]
        
    def move_disk_to(self, other_tower) -> None:
        """Move the smallest Disk from this Tower to other_tower.
        This method guarantees that after the move, the Disks in
        other_tower will be in the correct order. Invalid moves will not
        affect Disk ordering in self, either.
        """
        if all(disk != EMPTY for disk in other_tower):
            raise InvalidFirstMoveError('1st move must be from Tower 1.')
        
        this_tower_topmost_disk = self._get_and_remove_smallest_disk()
        
        # Because Disks have to go down as far as possible into
        # other_tower, we must put smallest_disk into the biggest index
        # of other_tower.disks where other_tower[smallest_disk] is
        # empty.
        #
        # Note that due to the way the Tower of Hanoi is structured,
        # there is never an instance in which we are trying to move
        # a Disk into a Tower already full of Disks. Only one Tower
        # can be full of Disks at any time.
        farthest_empty_index_down = (
            other_tower.get_bottommost_empty_space_index())
        
        other_tower_topmost_disk = other_tower.get_topmost_disk()
        
        if (other_tower_topmost_disk is not None and
        not this_tower_topmost_disk.is_smaller_than(other_tower_topmost_disk)):
            # Since we removed this_tower_smallest_disk at the
            # beginning, we have to put it back where it was before
            # now that we know the move we just made is invalid.
            self[self.index_of_smallest_disk] = this_tower_topmost_disk
            raise InvalidMoveError("can't move bigger Disks on top of "
                                   + 'smaller Disks.')
        
        # Put this_tower_topmost_disk as far up as possible in
        # other_tower
        other_tower[farthest_empty_index_down] = this_tower_topmost_disk
    
    def _get_and_remove_smallest_disk(self) -> Disk:
        """Get the smallest (topmost) Disk from self.disks, and replace
        it with EMPTY. Calling this method does not lead to an incorrect
        Disk ordering in self.disks.
        """
        smallest_disk = self.get_smallest_disk()
        
        self.index_of_smallest_disk = self.disks.index(smallest_disk)
        self[self.index_of_smallest_disk] = EMPTY
        return smallest_disk
    
    def get_smallest_disk(self) -> Disk:
        """Return the smallest (topmost) Disk from self.disks, without
        removing it from self.disks.
        """
        smallest_disk = None
        for disk in self:
            if disk != EMPTY:
                smallest_disk = disk
                break

        if smallest_disk is None:
            raise NoDisksError('the Tower is empty; it has no Disks.')
        
        return smallest_disk
    
    def get_bottommost_empty_space_index(self) -> int:
        """Return the biggest index of self.disks where
        self.disks[index] == EMPTY.
        """
        farthest_empty_index_down = -1
        
        for disk in self:
            if disk == EMPTY:
                farthest_empty_index_down += 1
            else:
                break
        return farthest_empty_index_down
    
    def get_topmost_disk(self) -> Disk or None:
        """Return the topmost Disk in the Tower if the Tower is not
        empty, else return None.
        """
        if any(disk != EMPTY for disk in self):
            other_tower_topmost_disk = self.get_smallest_disk()
        else:
            other_tower_topmost_disk = None
        return other_tower_topmost_disk
    
    def __getitem__(self, index: int):
        return self.disks[index]
    
    def __setitem__(self, index: int, value: int or Disk):
        self.disks[index] = value
        
    def __iter__(self):
        self._current_index = 0
        return self
    
    def __next__(self):
        if self._current_index < len(self.disks):
            current_disk = self[self._current_index]
            self._current_index += 1
            return current_disk
        raise StopIteration
