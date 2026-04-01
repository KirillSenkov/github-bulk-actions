# make-tree-python-clean.ps1
# Рисует "дерево" только выбранных путей, с игнором мусора.
# Вывод: tree.clean.txt в корне проекта.

$base = Get-Location

# Что показываем
$paths = @(
  "src",
  "tests",
  "alembic",
  "migrations",
  "main.py",
  "manage.py",
  "pyproject.toml",
  "uv.lock",
  "requirements.txt",
  "requirements-dev.txt",
  "setup.py",
  "README.md",
  ".env",
  ".env.example",
  ".gitignore"
)

# Что всегда игнорируем (имена + маски)
$skipNames = @(
  ".git", ".idea", ".vscode",
  "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
  ".venv", "venv", "env", # ".env",
  "dist", "build", ".tox", ".nox",
  ".eggs", ".egg-info", "*.egg-info",
  ".coverage", "htmlcov", ".cache"
)

$skipExtensions = @(".pyc", ".pyo")

$outFile = Join-Path $base "tree.clean.txt"
Remove-Item $outFile -ErrorAction SilentlyContinue

# Безопасные символы "дерева" через кодпоинты (в файле — чистый ASCII)
$CH_PIPE  = [char]0x2502  # │
$CH_TEE   = [char]0x251C  # ├
$CH_ELBOW = [char]0x2514  # └
$CH_HOR   = [char]0x2500  # ─

$BRANCH_MID  = "$CH_TEE$CH_HOR$CH_HOR "
$BRANCH_LAST = "$CH_ELBOW$CH_HOR$CH_HOR "
$PREF_MID    = "$CH_PIPE   "
$PREF_LAST   = "    "

function Should-SkipName {
  param([string]$name)
  foreach ($pat in $skipNames) {
    if ($name -like $pat) { return $true }
  }
  return $false
}

function Get-SortedChildren {
  param([string]$dir)

  $items = Get-ChildItem -LiteralPath $dir -Force -ErrorAction SilentlyContinue |
    Where-Object {
      $n = $_.Name
      if (Should-SkipName $n) { return $false }
      if (-not $_.PSIsContainer) {
        $ext = [System.IO.Path]::GetExtension($n)
        if ($skipExtensions -contains $ext) { return $false }
      }
      return $true
    } |
    Sort-Object `
      @{ Expression = { $_.PSIsContainer }; Descending = $true }, `
      @{ Expression = { $_.Name }; Descending = $false }

  return @($items)
}

function Write-Tree {
  param(
    [string]$dir,
    [string]$prefix = ""
  )

  $children = Get-SortedChildren $dir
  $count = $children.Count

  for ($i = 0; $i -lt $count; $i++) {
    $item = $children[$i]
    $isLast = ($i -eq $count - 1)

    $branch = if ($isLast) { $BRANCH_LAST } else { $BRANCH_MID }
    ($prefix + $branch + $item.Name) | Out-File -Append -Encoding utf8 $outFile

    if ($item.PSIsContainer) {
      $nextPrefix = if ($isLast) { $prefix + $PREF_LAST } else { $prefix + $PREF_MID }
      Write-Tree -dir $item.FullName -prefix $nextPrefix
    }
  }
}

foreach ($p in $paths) {
  $full = Join-Path $base $p
  if (-not (Test-Path -LiteralPath $full)) { continue }

  $p | Out-File -Append -Encoding utf8 $outFile

  if (Test-Path -LiteralPath $full -PathType Container) {
    Write-Tree -dir $full -prefix ""
  }
}