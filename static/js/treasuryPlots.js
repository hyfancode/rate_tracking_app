$('#treasury_types').on('change', function() {
	$.ajax({
		url         : '/treasuries/types',
		type        : 'GET',
		contentType : 'application/json;charset=UTF-8',
		data        : {
			selected : document.getElementById('treasury_types').value
		},
		dataType    : 'json',
		success     : function(data) {
			Plotly.newPlot(
				'treasury_charts',
				data,
				{
					xaxis      : {
						title      : 'Date',
						automargin : true
					},
					yaxis      : {
						title      : 'Percent',
						automargin : true
					},
					showlegend : true
				},
				{
					responsive : true
				}
			);
		}
	});
});
