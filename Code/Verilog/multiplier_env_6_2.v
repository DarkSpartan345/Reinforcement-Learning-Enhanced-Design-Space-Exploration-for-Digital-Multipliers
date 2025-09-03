
`timescale 1ns/1ps  
module multiplier (
input [1:0] A,
input [1:0] B,
output [3:0] P);

        // Generación de productos parciales
 wire pp0 = ((~A[0]) & (~B[1]));
 wire pp1 = ((A[0]) & (B[1]));
 wire pp2 = ((A[1]) & (B[1]));
 wire pp3 = ((A[1]) & (~B[0]));
 wire pp4 = ((~A[1]) & (~B[0]));

    // Suma de productos parciales
wire [1:0] columna4 = pp4 + pp0;
wire [1:0] columna3 = pp3 + pp1;
wire [1:0] columna1 = pp2;
assign P = (columna4 << 3) + (columna3 << 2) + (columna1 << 0);
endmodule