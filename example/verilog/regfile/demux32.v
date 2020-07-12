module demux32(
    input data,
    input [4:0] sel,
    output reg [31:0] out
);

always @(sel or data)
begin
out = 32'b0;
  case(sel)
    5'd0 : out[0] = data;

    5'd1 : out[1] = data;

    5'd2 : out[2] = data;

    5'd3 : out[3] = data;

    5'd4 : out[4] = data;

    5'd5 : out[5] = data;

    5'd6 : out[6] = data;

    5'd7 : out[7] = data;

    5'd8 : out[8] = data;

    5'd9 : out[9] = data;

    5'd10 : out[10] = data;

    5'd11 : out[11] = data;

    5'd12 : out[12] = data;

    5'd13 : out[13] = data;

    5'd14 : out[14] = data;

    5'd15 : out[15] = data;

    5'd16 : out[16] = data;

    5'd17 : out[17] = data;

    5'd18 : out[18] = data;

    5'd19 : out[19] = data;

    5'd20 : out[20] = data;

    5'd21 : out[21] = data;

    5'd22 : out[22] = data;

    5'd23 : out[23] = data;

    5'd24 : out[24] = data;

    5'd25 : out[25] = data;

    5'd26 : out[26] = data;

    5'd27 : out[27] = data;

    5'd28 : out[28] = data;

    5'd29 : out[29] = data;

    5'd30 : out[30] = data;

    5'd31 : out[31] = data;

    endcase
end

endmodule