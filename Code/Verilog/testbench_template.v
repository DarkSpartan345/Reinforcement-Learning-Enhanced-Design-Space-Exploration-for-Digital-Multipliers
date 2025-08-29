
`timescale 1ns/1ps
module tb_multiplier_8bit();
    // Señales de entrada
    reg [{regsI}:0] A;
    reg [{regsI}:0] B;
    
    // Señales de salida
    wire [{regsO}:0] P;

    // Instancia del módulo multiplicador
    multiplier uut (
        .A(A),
        .B(B),
        .P(P)
    );

    // Bloque inicial para pruebas
    initial begin
        
        {Test}
        // Terminar simulación
        $finish;
    end

    // Generación de forma de onda (opcional)
    initial begin
        $dumpfile("multiplier_8bit_tb.vcd");
        $dumpvars(0, tb_multiplier_8bit);
    end
endmodule