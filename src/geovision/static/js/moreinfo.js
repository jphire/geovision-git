var alignmentopen = false;
/*Function for showing the alignment of the read and the db-entry*/
function alignmentfunction(thisid) {
	if (alignmentopen) {
		closealignment();
	}
	if (alignmentopen == false){
		$.getJSON('/show_alignment', {id: thisid}, function (data) { /*get the json with the data*/
			if(data == null){
				return false;
			}
			alignmentopen = true;
			var part1 = $('<nobr>');
			var part2 = $('<nobr>');
			for ( i = 0; i < data.readseq.length; i++){
				if (i % 95 == 0 && i>0){
					part1.append('<br/>');
					part1.appendTo($('#alignment'));
					part1 = $('<nobr>');
					part2.appendTo($('#alignment'));
					part2 = $('<nobr>');
					$('<br/><br/>').appendTo($('#alignment'));
				}
				if (data.readseq.charAt(i) === data.dbseq.charAt(i)){
					part1 = part1.append('<span>' + data.readseq.charAt(i) + '</span>');
					part2 = part2.append('<span>' + data.dbseq.charAt(i) + '</span>');
				}
				else {
					part1 = part1.append('<span class=\'aligndifference\'>' + data.readseq.charAt(i) + '</span>');
					part2 = part2.append('<span class=\'aligndifference\'>' + data.dbseq.charAt(i) + '</span>');
				}
			}
			part1.appendTo($('#alignment'));
			$('<br/>').appendTo($('#alignment'));
			part2.appendTo($('#alignment'));
			$('#alignment').slideDown(300, function() { part1.fadeIn(); part2.fadeIn();
								var close = $('<div id = "closealign">Close</div>');
								$('#alignment').before(close);
								$('#alignment').css('margin-bottom', '10px');
			});
			return true;
		});
		return false;
	}
	else {
		return false;
	}
}
/*when the close button appears, it's se to work*/
$('#closealign').live('click', function() {
	closealignment();
});
/*Function to close the div-element showing the alignment*/
function closealignment () {
	if (alignmentopen == true){
		alignmentopen = false;
		$('#alignment').find('*').remove();/*!Hide all elements*/
		$('#closealign').remove();
		$('#alignment').css('margin-bottom', '0px');
		$('#alignment').slideUp();
	}
}

/* Function to list all names, reactions and pathways related to an enzyme in the right container */
function showEnzymeData (json){
	enzymes = {};
	rgraph.graph.eachNode(function(n) {
		if(n.data.type == 'enzyme')
			enzymes[n.id] = n;
	});
	ec = json.id;

	var html = '<br/>';
	if(json.reactions)
	{
		html += '<strong>Reactions of ' + ec + '</strong><br/>';
		html += $.map(json.reactions, function(reac){
			return 'R' + reac.id + ': ' + reac.name + ' <a target="_blank" href="http://www.genome.jp/dbget-bin/www_bget?r' + reac.id + '">[KEGG]</a><br/>'; }).join('');
	}
	// KEGG pathway url coloring params: pwnumber / ecnumber <TAB> #bgcol,#fgcol / ecnumber <TAB> #bgcol,fgcol ....
	if(json.pathways)
	{
		html += '<strong>Pathways of ' + ec + '</strong><br/>';
		html += $.map(json.pathways, function(pw){
			var pathwayEnzymes = $.grep(pw.enzymes, function(x) { return enzymes[x]; });
			var colorUrl = escape($.map(pathwayEnzymes, function(ec) { return ec + "\t" + enzymes[ec].data.color + ',#000000'; }).join('/'));
			return pw.id + ': ' + pw.name + '<a target="_blank" href="http://www.genome.jp/kegg-bin/show_pathway?map' + pw.id + '/' + colorUrl + '">[KEGG]</a><br/>'; }).join('');
	}

	names = json.names;

	html += '<strong>Other names of ' + ec + ':</strong><br/>';
	for (name in names){
		html = html + names[name] + '<br/>';
	}
	$('#names').html(html); /*#names is replaced fully when this is called for a new node*/
	return;
 }
