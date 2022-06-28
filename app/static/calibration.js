
let socket = io();
// When server emits an event of 'take this', display its message
socket.on('take this', (msg)=>{
    ///$('#declarer').text(msg.data);
});


socket.on('plots served', (msg)=>{
    //$('#declarer').text('FID & Spectrum plots should be served now...');
    // TODO use extend Traces so that the plot is UPDATED rather than REDRAWN - the goal is to stay zoomed in
    Plotly.newPlot('chart-left',JSON.parse(msg['fid']),{});
    Plotly.newPlot('chart-center',JSON.parse(msg['spectrum']),{});

} )

socket.on('fa plot served', (msg)=>{
    //$('#declarer').text('FA plot should be served now ... ');
    Plotly.newPlot('chart-right',JSON.parse(msg['fa_signal']),{});
})

$('#run-scan').click(()=> {
    socket.emit('run scans',{'data':'Start running scans'});
})

$('#stop-scan').click(()=>{
    socket.emit('stop scans',{'data':'Attempting to stop the scanning.'})
    }
)

$('#run-fa').click(()=>{
    socket.emit('run FA',{'data':'Start flip angle calibration.'})
})

$('#zero-shims').click(()=>{
    // Set shim values to zero
    $('#shimx').val(0.0)
    $('#shimy').val(0.0)
    $('#shimz').val(0.0)
    $('#shimx_val').val(0.0)
    $('#shimy_val').val(0.0)
    $('#shimz_val').val(0.0)

    // Send message to server to reset session shim values
    socket.emit('zero shims',{'data': 'Zeroing shim parameters!'})
})