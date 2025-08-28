
`timescale 1ns/1ps  
module multiplier (
input [1:0] A,
input [1:0] B,
output [3:0] P);

        // Generación de productos parciales
 wire pp0 = ((1) & (~B[0]));
 wire pp1 = ((A[0]) & (1));
 wire pp2 = ((A[1]) & (B[0]));
 wire pp3 = ((A[1]) & (B[1]));

    // Suma de productos parciales
wire [1:0] columna3 = pp3;
wire [1:0] columna2 = pp2;
wire [1:0] columna1 = pp1 + pp0;
assign P = (columna3 << 2) + (columna2 << 1) + (columna1 << 0);
endmodule