`timescale 1ns / 1ps

module Processor_main(
    input clk,
    input [7:0]gpi,
    output [7:0]gpo
);

wire [7:0]pc_addr;
wire [31:0]instr;
i_mem instr_memory(
    .address(pc_addr),
    .data(instr)
);

//Registers
reg [7:0]R0 = 0;
reg [7:0]R1 = 0;
reg [7:0]R2 = 0;
reg [7:0]R3 = 0;
reg [7:0]R4 = 0;
reg [7:0]R5 = 0;
wire [7:0]R6 = 8'd0;
reg [7:0]R7 = 0;

wire [7:0]R[7:0]; //Main Register Bus (ang) Glowny odsylacz do rejestrów (pl) 
assign R[0] = R0; 
assign R[1] = R1; 
assign R[2] = R2; 
assign R[3] = R3; 
assign R[4] = R4; 
assign R[5] = R5;
assign R[6] = R6; 
assign R[7] = R7; 


//instructions
wire [1:0] pc_op;
wire [2:0] d_op;
wire imm_op;
wire [1:0] alu_op;
wire [7:0]imm;
wire [2:0]ry_op;
wire [2:0]rx_op;
wire jnz;

assign pc_op = instr[25:24];
assign alu_op = instr[21:20];
assign rx_op = instr[18:16];
assign imm_op = instr[15];
assign ry_op = instr[14:12];
assign rd_op = instr[11];
assign d_op = instr[10:8];
assign imm = instr[7:0];
assign jnz = instr[19];

assign pc_addr = R7;

//RX_MUX
wire [7:0]rx_mux;
assign rx_mux = R[rx_op];

//RY_MUX
wire [7:0]ry_mux;
assign ry_mux = R[ry_op];

//IMM_MUX
wire [7:0]imm_mux;
assign  imm_mux = imm_op ? imm : ry_mux;

//ALU
//0-AND, 1-add, 2-zero_comp, 3-nothing
wire [7:0]alu_mux[3:0];
wire [7:0]alu_res;
wire cmp_res;
assign alu_mux[0] = rx_mux & imm_mux;
assign alu_mux[1] = rx_mux + imm_mux;
assign alu_mux[2] = rx_mux == 8'd0;
assign alu_mux[3] = imm_mux;
assign cmp_res = (rx_mux == 8'd0);
assign alu_res = alu_mux[alu_op];

//JUMPS
wire jump_cond;
assign jump_cond = pc_op[0] ? (cmp_res ^ pc_op[1]) : 1'b0; //pc_op[1] = 0 => R==0

//PC_MUX
wire [7:0]pc_mux;
assign pc_mux = jump_cond ? alu_res : R7+1;  

//DATA MEMORY
wire [7:0]mem_data;
d_mem data_memory(
    .address(alu_res), //8b
    .data(mem_data)
);

//RD_MUX
wire [7:0]rd_mux;
assign rd_mux = rd_op ? mem_data : alu_res;


always @(posedge clk)
begin
    //pc increment
    R7 <= pc_mux;
    
    //IO input
    R5 <= gpi;
    
    //to write register decoder
    case(d_op)
        0:R0 <= rd_mux;
        1:R1 <= rd_mux;
        2:R2 <= rd_mux;
        3:R3 <= rd_mux;
        4:R4 <= rd_mux;
    endcase
end
assign gpo[7:0] = R4[7:0];

endmodule
