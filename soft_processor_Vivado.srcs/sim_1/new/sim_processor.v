`timescale 1ns / 1ps

module sim_processor(
);

reg clk=1'b0;
initial
begin
    while(1) begin
        #5 clk=1'b0;
        #5 clk=1'b1;
    end
end

wire [7:0]LED;
reg [7:0]reg_sw = 0;
wire [7:0]SW;
assign SW = reg_sw;
top Procek(
    .clk100(clk),
    .sw(SW),
    .led(LED)
);

reg [31:0]CNT = 0;
always @(posedge clk)
begin
    CNT <= CNT+1;
end

endmodule
