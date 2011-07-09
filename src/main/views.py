from utils.decorators import render_to
from django.conf import settings
from main.models import Game, Cell, Player, CT_EMPTY, CT_WALL
from accounts.models import User
import random

@render_to('main/index.html')
def index(request):
    request.user.get_current_game()
    game = Game.objects.all()[:1].get()
    
    #generate(game,request.user)
    
    return {
        'ORBITED_STOMP_SOCKET': settings.ORBITED_STOMP_SOCKET,
        'ORBITED_HTTP_SOCKET': settings.ORBITED_HTTP_SOCKET
    }
    
def generate(game, user):
    width = 30
    height = 20
    
    for x in range(width):
        for y in range(height):
            cell = Cell(game=game)
            if random.random() < 0.2 and x not in (0, width-1) and y not in (0, height-1):
                cell.type = CT_WALL
            else:
                cell.type = CT_EMPTY
            print x, y
            cell.x = x
            cell.y = y
            cell.save()
    
    player = Player(user=user, game=game)
    player.cell = Cell.objects.get(x=0, y=0, game=game)
    player.save()
    
    user1 = User.objects.get(pk=2)
    player = Player(user=user1, game=game)
    player.cell = Cell.objects.get(x=width-1, y=0, game=game)
    player.save()
    
    user1 = User.objects.get(pk=3)
    player = Player(user=user1, game=game)
    player.cell = Cell.objects.get(x=0, y=height-1, game=game)
    player.save()
        
    user1 = User.objects.get(pk=4)
    player = Player(user=user1, game=game)
    player.cell = Cell.objects.get(x=width-1, y=height-1, game=game)
    player.save()            