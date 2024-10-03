import 'dart:io';

void main(List<String> arguments) async {
  // Verifica se foi passado um argumento para a mensagem de commit
  var commitMessage = arguments.isNotEmpty ? arguments.join(' ') : 'Atualização automática';

  // Verifica se há mudanças no diretório de trabalho
  var statusResult = await Process.run('git', ['status', '--porcelain']);
  
  if (statusResult.stdout.toString().trim().isEmpty) {
    print('Nada para commitar. O diretório está limpo.');
    exit(0);  // Sai do script se não houver mudanças
  }

  // Executa o comando git add .
  await _runCommand('git', ['add', '.']);

  // Executa o comando git commit -m "mensagem"
  await _runCommand('git', ['commit', '-m', commitMessage]);

  // Executa o comando git push
  await _runCommand('git', ['push', 'origin', 'main']);
}

Future<void> _runCommand(String command, List<String> args) async {
  var result = await Process.run(command, args);

  if (result.stdout.isNotEmpty) {
    print(result.stdout);
  }

  if (result.stderr.isNotEmpty) {
    print(result.stderr);
  }

  if (result.exitCode != 0) {
    print('Erro ao executar o comando: $command ${args.join(' ')}');
    exit(result.exitCode);
  }
}


// dart run push_to_github.dart "Minha mensagem de commit"