`include "example/verilog/regfile/registor32.v" 
`include "example/verilog/regfile/demux32.v" 
`include "example/verilog/regfile/mux32_32_1.v" 

module regfile(monitor_read1, monitor_read2, Input_clk, Input_WE, Input_RA1, Input_RA2, Input_WA, Input_WD);

input Input_clk, Input_WE;
input [4:0] Input_RA1, Input_RA2, Input_WA;
input [31:0] Input_WD;
output [31:0] monitor_read1, monitor_read2;

wire [31:0] r0_Q, r1_Q, r2_Q, r3_Q, r4_Q, r5_Q, r6_Q, r7_Q;
wire [7:0] dmux_out;
wire [23:0] dmux_open;

registor32 r0(.Q(r0_Q), .EN(dmux_out[0]), .clk(Input_clk), .D(Input_WD));
registor32 r1(.Q(r1_Q), .EN(dmux_out[1]), .clk(Input_clk), .D(Input_WD));
registor32 r2(.Q(r2_Q), .EN(dmux_out[2]), .clk(Input_clk), .D(Input_WD));
registor32 r3(.Q(r3_Q), .EN(dmux_out[3]), .clk(Input_clk), .D(Input_WD));
registor32 r4(.Q(r4_Q), .EN(dmux_out[4]), .clk(Input_clk), .D(Input_WD));
registor32 r5(.Q(r5_Q), .EN(dmux_out[5]), .clk(Input_clk), .D(Input_WD));
registor32 r6(.Q(r6_Q), .EN(dmux_out[6]), .clk(Input_clk), .D(Input_WD));
registor32 r7(.Q(r7_Q), .EN(dmux_out[7]), .clk(Input_clk), .D(Input_WD));
demux32 dmux(.out({dmux_out[7:0],dmux_open[23:0]}), .data(Input_WE), .sel(Input_WA));
mux32_32_1 m1(.out(monitor_read1), .data({r0_Q,r1_Q,r2_Q,r3_Q,r4_Q,r5_Q,r6_Q,r7_Q,768'b0}), .sel(Input_RA1));
mux32_32_1 m2(.out(monitor_read2), .data({r0_Q,r1_Q,r2_Q,r3_Q,r4_Q,r5_Q,r6_Q,r7_Q,768'b0}), .sel(Input_RA2));

endmodule