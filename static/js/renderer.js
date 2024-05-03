class Tile {
    constructor(color) {
        this.color = '';
        this.new_color = this.color;
    }
    set_color(color){
        this.new_color = color;
    }
}

class GameMap {
    constructor(width, height, ele_canvas) {
        this.canvas = /** @type {HTMLCanvasElement} */ ele_canvas;
        this.context = this.canvas.getContext("2d");
        this.width = width;
        this.height = height;
        let rect = ele_canvas.getBoundingClientRect()
        this.tile_width_px = rect.width / width;
        this.tile_height_px = rect.height / height;
        this.context.width = this.tile_width_px;
        this.context.height = this.tile_height_px;
        this.grid = [];
        for (let y = 0; y < this.height; y++) {
            this.grid[y] = [];
            for (let x = 0; x < this.width; x++) {
                this.grid[y][x] = new Tile('white');
            }
        }
    }
    reset_map() {
        for (let y = 0; y < this.height; y++) {
            for (let x = 0; x < this.width; x++) {
                this.grid[y][x].set_color('white');
            }
        }
    }

    render() {
        for (let y = 0; y < this.height; y++) {
            for (let x = 0; x < this.width; x++) {
                if (this.grid[y][x].color === this.grid[y][x].new_color) {
                    continue;
                }
                this.grid[y][x].color = this.grid[y][x].new_color;
                this.context.fillStyle = this.grid[y][x].color;
                this.context.fillRect(x * this.tile_width_px, y * this.tile_height_px, this.tile_width_px, this.tile_height_px);
            }

        }
    }
}
