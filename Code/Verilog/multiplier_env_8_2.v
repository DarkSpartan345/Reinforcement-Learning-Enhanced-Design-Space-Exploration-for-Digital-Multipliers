
`timescale 1ns/1ps  
module multiplier (
input [1:0] A,
input [1:0] B,
output [3:0] P);

        // Generación de productos parciales
 wire pp0 = ((A[1]) & (1));
 wire pp1 = ((A[1]) & (B[1]));

    // Suma de productos parciales
wire [1:0] columna4 = pp0;
wire [1:0] columna3 = pp1;
assign P = (columna4 << 3) + (columna3 << 2);
endmodule