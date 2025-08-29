
`timescale 1ns/1ps
module tb_multiplier_8bit();
    // Señales de entrada
    reg [1:0] A;
    reg [1:0] B;
    
    // Señales de salida
    wire [3:0] P;

    // Instancia del módulo multiplicador
    multiplier uut (
        .A(A),
        .B(B),
        .P(P)
    );

    // Bloque inicial para pruebas
    initial begin
        
        // Caso 0: Prueba aleatoria 0
                A = 8'd2;  // Acceso más eficiente con NumPy
                B = 8'd3;
                #10;
                $display("%d", P);
                //$display("A:%b,B:%b,res:%b",A,B P);

// Caso 1: Prueba aleatoria 1
                A = 8'd2;  // Acceso más eficiente con NumPy
                B = 8'd3;
                #10;
                $display("%d", P);
                //$display("A:%b,B:%b,res:%b",A,B P);

// Caso 2: Prueba aleatoria 2
                A = 8'd2;  // Acceso más eficiente con NumPy
                B = 8'd1;
                #10;
                $display("%d", P);
                //$display("A:%b,B:%b,res:%b",A,B P);

// Caso 3: Prueba aleatoria 3
                A = 8'd3;  // Acceso más eficiente con NumPy
                B = 8'd2;
                #10;
                $display("%d", P);
                //$display("A:%b,B:%b,res:%b",A,B P);

// Caso 4: Prueba aleatoria 4
                A = 8'd1;  // Acceso más eficiente con NumPy
                B = 8'd3;
                #10;
                $display("%d", P);
                //$display("A:%b,B:%b,res:%b",A,B P);

// Caso 5: Prueba aleatoria 5
                A = 8'd1;  // Acceso más eficiente con NumPy
                B = 8'd2;
                #10;
                $display("%d", P);
                //$display("A:%b,B:%b,res:%b",A,B P);

// Caso 6: Prueba aleatoria 6
                A = 8'd3;  // Acceso más eficiente con NumPy
                B = 8'd3;
                #10;
                $display("%d", P);
                //$display("A:%b,B:%b,res:%b",A,B P);

// Caso 7: Prueba aleatoria 7
                A = 8'd2;  // Acceso más eficiente con NumPy
                B = 8'd3;
                #10;
                $display("%d", P);
                //$display("A:%b,B:%b,res:%b",A,B P);

// Caso 8: Prueba aleatoria 8
                A = 8'd3;  // Acceso más eficiente con NumPy
                B = 8'd2;
                #10;
                $display("%d", P);
                //$display("A:%b,B:%b,res:%b",A,B P);

// Caso 9: Prueba aleatoria 9
                A = 8'd2;  // Acceso más eficiente con NumPy
                B = 8'd3;
                #10;
                $display("%d", P);
                //$display("A:%b,B:%b,res:%b",A,B P);

// Caso 10: Prueba aleatoria 10
                A = 8'd1;  // Acceso más eficiente con NumPy
                B = 8'd1;
                #10;
                $display("%d", P);
                //$display("A:%b,B:%b,res:%b",A,B P);

// Caso 11: Prueba aleatoria 11
                A = 8'd3;  // Acceso más eficiente con NumPy
                B = 8'd2;
                #10;
                $display("%d", P);
                //$display("A:%b,B:%b,res:%b",A,B P);

// Caso 12: Prueba aleatoria 12
                A = 8'd2;  // Acceso más eficiente con NumPy
                B = 8'd1;
                #10;
                $display("%d", P);
                //$display("A:%b,B:%b,res:%b",A,B P);

// Caso 13: Prueba aleatoria 13
                A = 8'd3;  // Acceso más eficiente con NumPy
                B = 8'd3;
                #10;
                $display("%d", P);
                //$display("A:%b,B:%b,res:%b",A,B P);

// Caso 14: Prueba aleatoria 14
                A = 8'd1;  // Acceso más eficiente con NumPy
                B = 8'd1;
                #10;
                $display("%d", P);
                //$display("A:%b,B:%b,res:%b",A,B P);

// Caso 15: Prueba aleatoria 15
                A = 8'd2;  // Acceso más eficiente con NumPy
                B = 8'd3;
                #10;
                $display("%d", P);
                //$display("A:%b,B:%b,res:%b",A,B P);

// Caso 16: Prueba aleatoria 16
                A = 8'd3;  // Acceso más eficiente con NumPy
                B = 8'd3;
                #10;
                $display("%d", P);
                //$display("A:%b,B:%b,res:%b",A,B P);

// Caso 17: Prueba aleatoria 17
                A = 8'd1;  // Acceso más eficiente con NumPy
                B = 8'd1;
                #10;
                $display("%d", P);
                //$display("A:%b,B:%b,res:%b",A,B P);

// Caso 18: Prueba aleatoria 18
                A = 8'd1;  // Acceso más eficiente con NumPy
                B = 8'd2;
                #10;
                $display("%d", P);
                //$display("A:%b,B:%b,res:%b",A,B P);

// Caso 19: Prueba aleatoria 19
                A = 8'd3;  // Acceso más eficiente con NumPy
                B = 8'd2;
                #10;
                $display("%d", P);
                //$display("A:%b,B:%b,res:%b",A,B P);

        // Terminar simulación
        $finish;
    end

    // Generación de forma de onda (opcional)
    initial begin
        $dumpfile("multiplier_8bit_tb.vcd");
        $dumpvars(0, tb_multiplier_8bit);
    end
endmodule