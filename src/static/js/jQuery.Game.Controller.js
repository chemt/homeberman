jQuery.Game = jQuery.Game || {};

jQuery.Game.Controller = jQuery.inherit(jQuery.util.Observable, {
    map: null, //jQuery.Game.Map
    player: null, //jQuery.Game.Player
    enemies: {},
    bombs: {},
    constructor : function(config){
        jQuery.extend(this, config);
        jQuery.Game.Controller.superclass.constructor.call(this, config);
        this.init();
    },
    init: function(){
        GameApi.load_players(this.initPlayers, this);
        this.map.on('cellclick', this.onCellClick, this);
        var that = this;
        jQuery('body').keypress(function(event){that.onKeyPress(event); return false;});
    },
    initPlayers: function(data){
        this.player = new jQuery.Game.Player({
            name: data.player.name,
            cell: this.map.getCell(data.player.x, data.player.y)
        });
        for (var i=0, len=data.enemies.length; i<len; i++){
            var e = data.enemies[i];
            this.enemies[e.id] = new jQuery.Game.Enemy({
                name: e.name,
                cell: this.map.getCell(e.x, e.y)
            });
        }
    },
    canMove: function(cell){
        var dx = Math.abs(cell.x-this.player.cell.x);
        var dy = Math.abs(cell.y-this.player.cell.y);
        return ( 
            cell.isMoveable() && 
            dx <= 1 && 
            dx <= 1 &&
            dx != dy
        )
    },
    onKeyPress: function(event){
        switch(event.which){
            case 32:
            this.createBomb();
            break;
            case 119:
            this.move(0, -1);
            break;
            case 115:
            this.move(0, 1);
            break;
            case 97:
            this.move(-1, 0);
            break;
            case 100:
            this.move(1, 0);
            break;
        }
    },
    move: function(dx, dy){
        var cell = this.player.cell;
        var new_cell = this.map.getCell(cell.x+dx, cell.y+dy);
        if (new_cell){
            this.onCellClick(new_cell);
        }
    },
    createBomb: function(){
        if (this.player.isDead) return;
        
        var bomb = new jQuery.Game.Bomb({
            cell: this.player.cell
        });
        this.bombs[bomb.key] = bomb;
    },
    onCellClick: function(cell, map){
        if ( ! this.player.isDead && this.canMove(cell)){
            this.player.setCell(cell);
        }
    }
});