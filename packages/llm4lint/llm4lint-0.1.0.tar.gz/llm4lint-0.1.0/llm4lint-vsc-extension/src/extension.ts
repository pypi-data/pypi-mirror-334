// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import ollama from 'ollama';

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "llm4lint-vsc" is now active!');
	// The command has been defined in the package.json file
	// Now provide the implementation of the command with registerCommand
	// The commandId parameter must match the command field in package.json
	const get_lints_cmd = vscode.commands.registerCommand('llm4lint-vsc.get_lints', (cmd_context) => {
		let llm_diagnostics = vscode.languages.createDiagnosticCollection("LLM4Lint");
		llm_diagnostics.clear();
		const prompt = "Perform linting on the given code. Specify output in format: <line_number> - <type>: <issue>\n";
		let file_uri = vscode.Uri.file(cmd_context["path"]);
		// vscode.commands.executeCommand("vscode.open", file_uri);
		vscode.workspace.openTextDocument(file_uri).then(async (document) => {
			let code = document.getText();
			let code_lines = code.split("\n");
			let code_with_lines = "";
			for (let index = 0; index < code_lines.length; index++) {
				const line = code_lines[index];
				code_with_lines += String(index+1) + "   " + line + "\n";
			}
			const response = await ollama.chat({
				model: 'llm4lint7b',
				messages: [{ role: 'user', content: prompt + code_with_lines }],
			})
			//console.log(response.message.content)
			const output_lines = response.message.content.split("\n")

			// display diagnostics
			let _diagnostics = [];
			const _severity = vscode.DiagnosticSeverity.Warning;
			for (let index = 0; index < output_lines.length; index++) {
				const line = output_lines[index];
				const lno = Number(line.at(0));
				// console.log(lno) lineno is off by +1 for some reason...
				if (!isNaN(lno)) {
					const start_char = code_lines.at(lno)?.charAt(0)
					let end_char = code_lines.at(lno)?.length
					end_char ??= 0
					const file_diagnostic = new vscode.Diagnostic(new vscode.Range(lno-1,0,lno-1,end_char), line.slice(4), _severity);
					_diagnostics.push(file_diagnostic);
				}
			}
			if ((_diagnostics.length) == 0) {
				vscode.window.showInformationMessage("Clean Code: No Issues Detected");
			}
			llm_diagnostics.set(file_uri, _diagnostics);
			context.subscriptions.push(llm_diagnostics);
		  });
		vscode.window.showInformationMessage('Linting...');
	});
	const init_shell_cmd = vscode.commands.registerCommand('llm4lint-vsc.init_shell', (cmd_context) => {
		const script = "llm4lint " + "-i " + cmd_context["path"];
		let terminal = vscode.window.createTerminal({
			name: "LLM4Lint-7B",
			hideFromUser: false,
		});
		terminal.sendText(script)
		terminal.show()
		vscode.window.showInformationMessage("If Shell fails to launch install using: 'pip install llm4lint'");
	});

	context.subscriptions.push(get_lints_cmd);
	context.subscriptions.push(init_shell_cmd);
}

// This method is called when your extension is deactivated
export function deactivate() {}
