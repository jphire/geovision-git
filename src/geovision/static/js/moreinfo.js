/*Function for showing the alignment of the read and the db-entry*/
function alignmentfunction(thisid) {
	$.getJSON('/show_alignment', {id: thisid}, function (data) { /*get the json with the data*/
		if(data == null){
			return false;
		}
		alignment = $('<div class="alignment"></div>');
		var close = $('<div id = "closealign">Close</div>');
		close.appendTo(alignment);
		$('<p>Alignmentid: '+thisid+'</p>').appendTo(alignment);
		for ( i = 0; i < data.readseq.length; i++){
			var alignmentclass = "";
			if (data.readseq.charAt(i) === data.dbseq.charAt(i)){
				alignmentclass = " alignsimilarity";
			}
			else {
				alignmentclass="";
			}
			var a = $('<span class="alignmentpart'+ alignmentclass +'">' + data.readseq.charAt(i) +'\n'+ data.dbseq.charAt(i)+ '</span>');
			a.appendTo(alignment);
		}
		$('#alignment').before(alignment);
		alignment.slideDown(300, function() {
							alignment.css('margin-bottom', '10px');
		});
		return true;
	});
	return false;
}
/*when the close button appears, it's se to work*/
$('#closealign').live('click', function() {
	closealignment(this);
});
/*Function to close the div-element showing the alignment*/
function closealignment (button) {
		button = $(button);
		var alignment = button.parent();
		$(alignment).find('*').remove();/*!Hide all elements*/
		$(button).remove();
		$(alignment).css('margin-bottom', '0px');
		$(alignment).slideUp();
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
	/*
	if(json.reactions)
	{
		html += '<strong>Reactions of ' + ec + '</strong><br/>';
		html += $.map(json.reactions, function(reac){
			return 'R' + reac.id + ': ' + reac.name + ' <a target="_blank" href="http://www.genome.jp/dbget-bin/www_bget?r' + reac.id + '">[KEGG]</a><br/>'; }).join('');
	}
	*/
	// KEGG pathway url coloring params: pwnumber / ecnumber <TAB> #bgcol,#fgcol / ecnumber <TAB> #bgcol,fgcol ....
	if(json.pathways)
	{
		html += '<strong>Pathways of ' + ec + '</strong><br/>';
		html += $.map(json.pathways, function(pw){
			var pathwayEnzymes = $.grep(pw.enzymes, function(x) { return enzymes[x]; });
			var colorUrl = escape($.map(pathwayEnzymes, function(ec) { return ec + "\t" + enzymes[ec].data.color + ',#000000'; }).join('/'));
			return  '<a target="_blank" href="http://www.genome.jp/kegg-bin/show_pathway?map' + pw.id + '/' + colorUrl + '">' + pw.id + ': ' + pw.name + '</a><br/>'; }).join('');
	}

	names = json.names;

	html += '<strong>Other names of ' + ec + ':</strong><br/>';
	for (name in names){
		html = html + names[name] + '<br/>';
	}
	$('#names').html(html); /*#names is replaced fully when this is called for a new node*/
	return;
 }
