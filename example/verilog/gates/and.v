module and_2_1(in1, in2, out);
input [1:0] in1, in2;
output [1:0] out;

assign out[0] = in1[0] & in2[0];
assign out[1] = in1[1] & in2[1];

endmodule