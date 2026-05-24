import sys
import re
from bs4 import BeautifulSoup

def audit_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    content = soup.find('main') or soup.body
    if not content:
        return []
    
    # Remove code blocks, preformatted text, and hidden elements
    for s in content(['script', 'style', 'pre', 'code']):
        s.decompose()
        
    # Also remove quarto-specific cell components if they aren't part of narrative
    for s in content.find_all(class_=re.compile(r'cell-code|quarto-appendix-contents|quarto-figure')):
        s.decompose()

    text = content.get_text(separator=' ')
    
    # Improved pattern: match numbers ending in .0
    pattern = re.compile(r'(\b[\d,]+\.0\b)')
    
    results = []
    for match in pattern.finditer(text):
        full_match = match.group(1)
        start = max(0, match.start() - 40)
        end = min(len(text), match.end() + 40)
        context = text[start:end].replace('\n', ' ').strip()
        
        # --- FILTERS ---
        if re.search(r'Software\s+[\d,]+\.0', context):
            continue
        if re.search(r'in\s+20\d{2}\.0', context) or re.search(r'year\s+20\d{2}\.0', context):
            continue
        # Product / protocol version numbers (not computed narrative values)
        if re.search(
            r'(?:Industry|PyTorch|TensorFlow|NVLink|CUDA|SciPy|PCIe|InfiniBand|DOI|CO;)\s*[\d,]*\.0',
            context,
            re.I,
        ):
            continue
        if re.search(r'CO;\d+\.0', context):
            continue
        if re.search(r'rounds to [\d,]+\.0', context, re.I):
            continue
        if re.search(r'\\(?:approx|times|exp|lbrack|rbrack|hat|mathbf|partial|mathcal|frac|begin|end)', context):
            continue
        if re.search(r'\d+\.0\s*(?:μs|us|percent vs|percent test error)', context, re.I):
            continue
        if re.search(r'(?:AID-|::AID-)[^\s]*\d+\.0', context):
            continue
        if re.search(r'\d+\.0 in less optimized', context, re.I):
            continue
        if re.search(r'\\(?:cdot|;|,|\(|\[|hat|mathbf|partial|mathcal|frac|begin|end|approx|times|exp|lbrack|rbrack)', context):
            continue
        if re.search(r'\\text\{[^}]*\d+\.0', context):
            continue
        if re.search(r'PyTorch\s+[\d,]+\.0', context):
            continue
        if re.search(r"(?:KFLOPs|MFLOPs|GFLOPs|TFLOPs|TFLOP/s|TB/s|GB/s| billion FLOPs| pJ)\b", context):
            continue
        if re.search(r"\d+\.0\s*M\b", context):
            continue
        if "FLOP/byte" in context:
            continue
        # LaTeX/math literals already rendered in prose
        if re.search(r'[\[\(=]\s*[\d,]+\.0', context):
            continue
        if re.search(r'1\.0\s*\(perfect\)', context):
            continue
        if re.search(r'\[0\.5,\s*2\.0\]', context):
            continue
        
        # Filter out common CSS units if they leaked
        if full_match in ['1.0', '2.0', '1.5'] and ('em' in context or 'px' in context):
            continue

        results.append({
            'value': full_match,
            'context': context
        })
        
    return results

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 audit_html.py <path_to_html>")
        sys.exit(1)
    
    issues = audit_html(sys.argv[1])
    if not issues:
        print("CLEAN")
    else:
        for issue in issues:
            print(f"FOUND: {issue['value']} | Context: ...{issue['context']}...")
