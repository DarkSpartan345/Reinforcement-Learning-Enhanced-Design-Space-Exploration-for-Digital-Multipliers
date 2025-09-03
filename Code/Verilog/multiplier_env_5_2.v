
`timescale 1ns/1ps  
module multiplier (
input [1:0] A,
input [1:0] B,
output [3:0] P);

        // Generación de productos parciales
 wire pp0 = ((A[0]) & (B[0]));

    // Suma de productos parciales
wire [1:0] columna3 = pp0;
assign P = (columna3 << 2);
endmodule