#include <stdbool.h>
bool braille_array[][6] = {
/* pin ordering:
 * 0 5
 * 1 4
 * 2 3 
 */
{0, 0, 0, 0, 0, 0}, // SPACE
{0, 1, 1, 0, 1, 0}, // ! 
{0, 0, 1, 1, 1, 0}, // " this is really open quote, change later to parse 
{0, 0, 1, 1, 1, 1}, // # requires 2 cells (right straight down)
{0, 1, 0, 1, 1, 0}, // $ requires 2 cells (top right)
{0, 0, 0, 0, 0, 0}, // % percent is actually 3 cells....this is a placeholder
{1, 1, 1, 1, 0, 1}, // & requires 2 cells (top right)
{0, 0, 1, 0, 0, 0}, // '
{0, 1, 1, 1, 1, 0}, // ( 
{0, 1, 1, 1, 1, 0}, // ) 
{0, 0, 1, 0, 1, 0}, // * requires 2 cells
{0, 1, 1, 0, 1, 0}, // + requires 2 cells
{0, 1, 0, 0, 0, 0}, // , 
{0, 0, 1, 1, 0, 0}, // - 
{0, 1, 0, 1, 1, 0}, // . 
{0, 0, 1, 0, 0, 1}, // / requires 2 cells, placeholder
{0, 1, 0, 0, 1, 1}, // 0 requires 2 cells
{1, 0, 0, 0, 0, 0}, // 1 requires 2 cells
{1, 1, 0, 0, 0, 0}, // 2 requires 2 cells
{1, 0, 0, 0, 0, 1}, // 3 requires 2 cells
{1, 0, 0, 0, 1, 1}, // 4 requires 2 cells
{1, 0, 0, 0, 1, 0}, // 5 requires 2 cells
{1, 1, 0, 0, 0, 1}, // 6 requires 2 cells
{1, 1, 0, 0, 1, 1}, // 7 requires 2 cells
{1, 1, 0, 0, 1, 0}, // 8 requires 2 cells
{0, 1, 0, 0, 0, 1}, // 9 requires 2 cells
{0, 1, 0, 0, 1, 0}, // : 
{0, 1, 1, 0, 0, 0}, // ; 
{0, 0, 0, 0, 0, 0}, // < requires 2 cells, placeholder 
{0, 0, 0, 0, 0, 0}, // = requires 2 cells, placeholder 
{0, 0, 0, 0, 0, 0}, // > requires 2 cells, placeholder 
{0, 1, 1, 1, 0, 0}, // ?
{0, 0, 1, 1, 0, 1}, // @ requires 2 cells
{1, 0, 0, 0, 0, 0}, // A 
{1, 1, 0, 0, 0, 0}, // B 
{1, 0, 0, 0, 0, 1}, // C
{1, 0, 0, 0, 1, 1}, // D 
{1, 0, 0, 0, 1, 0}, // E
{1, 1, 0, 0, 0, 1}, // F 
{1, 1, 0, 0, 1, 1}, // G 
{1, 1, 0, 0, 1, 0}, // H 
{0, 1, 0, 0, 0, 1}, // I 
{0, 1, 0, 0, 1, 1}, // J 
{1, 0, 1, 0, 0, 0}, // K 
{1, 1, 1, 0, 0, 0}, // L 
{1, 0, 1, 0, 0, 1}, // M 
{1, 0, 1, 0, 1, 1}, // N 
{1, 0, 1, 0, 1, 0}, // O 
{1, 1, 1, 0, 0, 1}, // P 
{1, 1, 1, 0, 1, 1}, // Q 
{1, 1, 1, 0, 1, 0}, // R 		
{0, 1, 1, 0, 0, 1}, // S 
{0, 1, 1, 0, 1, 1}, // T 
{1, 0, 1, 1, 0, 0}, // U 
{1, 1, 1, 1, 0, 0}, // V 
{0, 1, 0, 1, 1, 1}, // W
{1, 0, 1, 1, 0, 1}, // X 
{1, 0, 1, 1, 1, 1}, // Y 
{1, 0, 1, 1, 1, 0}, // Z 	
}; 
