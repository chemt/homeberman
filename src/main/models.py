# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from django.db import models
from accounts.models import User
import time

MOVE_TIME = 1

GS_WAITING = 0
GS_PLAYING = 1
GS_FINISHED = 2

GAME_STATUS_CHOICES = (
    (GS_WAITING, _("Waiting for players")),
    (GS_PLAYING, _("Playing")),
    (GS_FINISHED, _("Finished")),
)

GS_SMALL = "small"
GS_MEDIUM = "medium"
GS_BIG = "big"
GAME_SIZE_CHOICES = (
    (GS_SMALL, _(u"Small")),
    (GS_MEDIUM, _(u"Medium")),
    (GS_BIG, _(u"Big")),
)

class Player(models.Model):
    user = models.ForeignKey(User)
    cell = models.ForeignKey('Cell')
    game = models.ForeignKey('Game')
    is_dead = models.BooleanField(default=False)
    last_move_time = models.BigIntegerField(default=0)
    
    class Meta:
        unique_together = (('game', 'user'),)
    
    def update_move_time(self):
        self.last_move_time = time.time()
        self.save()
    
    def can_move(self):
        return not self.is_dead and \
            (time.time() - self.last_move_time) > MOVE_TIME
    
    def move_to(self, x, y):
        if not self.can_move():
            return False
        
        cell = self.game.get_cell(x=x, y=y)
        
        if not cell:
            return False
        
        self.update_move_time()
        
        self.cell = cell
        self.save()
        
        return True
    
    def record(self):
        return {
            'id': self.pk,
            'name': unicode(self.user),
            'x': self.cell.x,
            'y': self.cell.y                     
        }

class Game(models.Model):
    name = models.CharField(max_length=140, null=True, blank=True)
    status = models.IntegerField(default=0, choices=GAME_STATUS_CHOICES)
    max_players = models.PositiveIntegerField(default=10)
    size = models.CharField(default='small', choices=GAME_SIZE_CHOICES, max_length=10)
    winner = models.ForeignKey(Player, related_name='winned_games', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    started = models.DateTimeField(null=True, blank=True)
    
    def get_cell(self, x, y):
        try:
            return self.cells.get(x=x, y=y)
        except models.ObjectDoesNotExist:
            pass
    
    def get_size(self):
        if self.size == GS_SMALL:
            return 20, 15
                
        if self.size == GS_MEDIUM:
            return 25, 20
        
        if self.size == GS_BIG:
            return 30, 20      
    
CT_EMPTY = 0
CT_WALL = 1

CELL_TYPE_CHOICES = (
    (CT_EMPTY, 'empty'),
    (CT_WALL, 'wall')
)

class Cell(models.Model):
    game = models.ForeignKey(Game, related_name='cells')
    x = models.IntegerField()
    y = models.IntegerField()
    type = models.IntegerField(default=CT_EMPTY, choices=CELL_TYPE_CHOICES)
    
    class Meta:
        unique_together = (('game', 'x', 'y'),)
    
    def key(self):
        return '%s_%s' % (self.x, self.y)
    
    def record(self):
        return {
            'type': self.type
        }
    