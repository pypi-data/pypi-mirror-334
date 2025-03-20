import torch
import time
import json
import argparse
import numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer
from rouge_score import rouge_scorer
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import nltk

# Download necessary NLTK data
try:
    nltk.download('punkt', quiet=True)
except:
    print("NLTK download failed, but proceeding anyway")

# Default evaluation questions if no dataset is provided
DEFAULT_EVAL_QUESTIONS = [
    {
        "instruction": "What are the different classifications of the drug Imatinib?",
        "input": "",
        "reference": "Imatinib (Gleevec/Glivec) can be classified as: 1) a tyrosine kinase inhibitor (TKI), 2) a targeted therapy, 3) an antineoplastic agent, 4) a BCR-ABL inhibitor, 5) a c-KIT inhibitor, and 6) a PDGFR inhibitor. It's also categorized by its therapeutic use for chronic myeloid leukemia (CML), gastrointestinal stromal tumors (GIST), and other rare cancers."
    },
    {
        "instruction": "Describe the mechanism of action for metformin.",
        "input": "",
        "reference": "Metformin decreases hepatic glucose production through inhibition of the mitochondrial respiratory chain (complex I) and activation of AMPK (AMP-activated protein kinase). This leads to reduced gluconeogenesis and glycogenolysis. It also increases peripheral glucose uptake in skeletal muscle, reduces intestinal glucose absorption, and improves insulin sensitivity by increasing insulin receptor tyrosine kinase activity and insulin receptor expression."
    },
    {
        "instruction": "What are the pharmacokinetic properties of atorvastatin?",
        "input": "",
        "reference": "Atorvastatin has oral bioavailability of approximately 14%, high protein binding (>98%), extensive first-pass metabolism in the liver via CYP3A4, and is primarily eliminated through biliary excretion. Its mean plasma elimination half-life is approximately 14 hours, but the inhibitory effect on HMG-CoA reductase lasts 20-30 hours due to active metabolites. It is best absorbed under fasting conditions and has dose-proportional pharmacokinetics."
    },
    {
        "instruction": "Describe the chemical structure of sildenafil.",
        "input": "",
        "reference": "Sildenafil (C22H30N6O4S) is a pyrazolopyrimidinone derivative. Its chemical structure consists of a pyrazolopyrimidinone core with a methylpiperazine ring, a sulfonamide group, and an ethoxy group. The IUPAC name is 5-{2-ethoxy-5-[(4-methylpiperazin-1-yl)sulfonyl]phenyl}-1-methyl-3-propyl-1,6-dihydro-7H-pyrazolo[4,3-d]pyrimidin-7-one."
    },
    {
        "instruction": "What clinical trials have been conducted for the drug pembrolizumab?",
        "input": "",
        "reference": "Key clinical trials for pembrolizumab include KEYNOTE-001 (first-in-human study), KEYNOTE-006 (melanoma), KEYNOTE-024 and KEYNOTE-042 (first-line NSCLC), KEYNOTE-189 (non-squamous NSCLC), KEYNOTE-407 (squamous NSCLC), KEYNOTE-048 (head and neck cancer), KEYNOTE-057 (bladder cancer), KEYNOTE-181 (esophageal cancer), KEYNOTE-426 (renal cell carcinoma), and KEYNOTE-522 (triple-negative breast cancer). These trials established its efficacy across multiple cancer types, leading to numerous FDA approvals."
    }
]

def load_jsonl_dataset(file_path, max_samples=None):
    """
    Load evaluation dataset from a JSONL file.
    
    Args:
        file_path: Path to the JSONL file
        max_samples: Maximum number of samples to load (None for all)
        
    Returns:
        List of evaluation samples
    """
    samples = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    sample = json.loads(line.strip())
                    # Handle different dataset formats
                    if "output" in sample and "reference" not in sample:
                        sample["reference"] = sample["output"]
                    samples.append(sample)
                except json.JSONDecodeError:
                    print(f"Warning: Could not parse line: {line[:50]}...")
                    continue
                
        if max_samples is not None and max_samples < len(samples):
            # Use random sampling to get a diverse subset
            import random
            random.seed(42)
            samples = random.sample(samples, max_samples)
            
        print(f"Loaded {len(samples)} samples from {file_path}")
        return samples
    except Exception as e:
        print(f"Error loading dataset from {file_path}: {e}")
        return None

def evaluate_model(model_path="./fine_tuned_model", 
                  evaluation_file=None, 
                  max_samples=None,
                  max_new_tokens=200,
                  output_file=None):
    """
    Evaluate a fine-tuned model using the provided evaluation dataset.
    
    Args:
        model_path: Path to the fine-tuned model
        evaluation_file: Path to the evaluation JSONL file (None to use default questions)
        max_samples: Maximum number of samples to evaluate
        max_new_tokens: Maximum number of new tokens to generate
        output_file: Path to save the evaluation results (None for auto-generated)
    """
    # Check for MPS availability
    if torch.backends.mps.is_available():
        device = torch.device("mps")
        print("Using MPS device (Apple Silicon GPU)")
    else:
        device = torch.device("cpu")
        print("MPS not available, using CPU instead")

    print(f"Loading model from {model_path}...")

    # Load the tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    tokenizer.pad_token = tokenizer.eos_token

    # Optional: Perform a warmup step to initialize MPS cache
    if device.type == "mps":
        print("Performing MPS warmup...")
        dummy_input = torch.zeros(1, 1, device=device)
        dummy_output = dummy_input * 2
        del dummy_input, dummy_output
        torch.mps.synchronize()

    # Load the model
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        device_map="auto" if device.type != "mps" else None,
        torch_dtype=torch.float32,
    )

    # Move model to device if using MPS
    if device.type == "mps":
        model = model.to(device)
        
    print(f"Model loaded successfully on {device}")

    # Initialize metrics
    rouge_scorer_instance = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    smooth = SmoothingFunction().method1

    # Load evaluation questions
    if evaluation_file:
        eval_questions = load_jsonl_dataset(evaluation_file, max_samples)
        if not eval_questions:
            print("Using default evaluation questions as fallback")
            eval_questions = DEFAULT_EVAL_QUESTIONS
    else:
        print("No evaluation file provided, using default evaluation questions")
        eval_questions = DEFAULT_EVAL_QUESTIONS
        
    if max_samples and len(eval_questions) > max_samples:
        eval_questions = eval_questions[:max_samples]

    # Results storage
    results = {
        "predictions": [],
        "metrics": {
            "rouge1": [],
            "rouge2": [],
            "rougeL": [],
            "bleu": [],
            "generation_time": []
        },
        "summary": {},
        "config": {
            "model_path": model_path,
            "evaluation_file": evaluation_file,
            "device": str(device),
            "max_new_tokens": max_new_tokens,
            "num_samples": len(eval_questions)
        }
    }
    
    # Evaluate on each question
    print(f"Starting evaluation on {len(eval_questions)} test questions...")
    for idx, sample in enumerate(eval_questions):
        instruction = sample.get("instruction", "")
        input_text = sample.get("input", "")
        reference = sample.get("reference", "")
        
        # Prepare prompt
        if input_text:
            prompt = f"{instruction}\n{input_text}\nAssistant: "
        else:
            prompt = f"{instruction}\nAssistant: "
        
        # Generate prediction
        inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, max_length=512)
        inputs = {key: value.to(device) for key, value in inputs.items()}
        
        # Measure generation time
        start_time = time.time()
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                temperature=0.1,
            )
        
        # Calculate timing
        gen_time = time.time() - start_time
        tokens_generated = outputs.shape[1] - inputs["input_ids"].shape[1]
        tokens_per_second = tokens_generated / gen_time
        
        # Decode prediction
        full_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
        prediction = full_output[len(prompt):].strip()
        
        # Skip empty predictions
        if not prediction:
            print(f"Warning: Empty prediction for sample {idx}")
            continue
        
        # Calculate metrics only if reference is provided
        if reference:
            rouge_scores = rouge_scorer_instance.score(prediction, reference)
            
            try:
                reference_tokens = [tokenize_for_bleu(reference)]
                prediction_tokens = tokenize_for_bleu(prediction)
                bleu_score = sentence_bleu(reference_tokens, prediction_tokens, smoothing_function=smooth)
            except Exception as e:
                print(f"Error calculating BLEU: {e}")
                bleu_score = 0
                
            # Save metrics
            results["metrics"]["rouge1"].append(rouge_scores["rouge1"].fmeasure)
            results["metrics"]["rouge2"].append(rouge_scores["rouge2"].fmeasure)
            results["metrics"]["rougeL"].append(rouge_scores["rougeL"].fmeasure)
            results["metrics"]["bleu"].append(bleu_score)
            
            metrics_data = {
                "rouge1": rouge_scores["rouge1"].fmeasure,
                "rouge2": rouge_scores["rouge2"].fmeasure,
                "rougeL": rouge_scores["rougeL"].fmeasure,
                "bleu": bleu_score
            }
        else:
            print(f"Warning: No reference provided for sample {idx}, skipping metrics calculation")
            metrics_data = None
            
        results["metrics"]["generation_time"].append(gen_time)
        
        # Save prediction
        results["predictions"].append({
            "sample_id": idx,
            "instruction": instruction,
            "input": input_text,
            "prediction": prediction,
            "reference": reference,
            "tokens_generated": tokens_generated,
            "generation_time_seconds": gen_time,
            "tokens_per_second": tokens_per_second,
            "metrics": metrics_data
        })
        
        # Print detailed results for each question
        print(f"\n===== QUESTION {idx+1} =====")
        print(f"Instruction: {instruction}")
        if input_text:
            print(f"Input: {input_text}")
        print("\nModel response:")
        print(f"{prediction}")
        if reference:
            print("\nReference answer:")
            print(f"{reference}")
            print("\nMetrics:")
            if metrics_data:
                for metric, value in metrics_data.items():
                    print(f"{metric}: {value:.4f}")
        print(f"Generated {tokens_generated} tokens in {gen_time:.2f}s ({tokens_per_second:.2f} tokens/sec)")
    
    # Calculate summary metrics if we have metrics
    if results["metrics"]["rouge1"]:
        results["summary"] = {
            "rouge1": np.mean(results["metrics"]["rouge1"]),
            "rouge2": np.mean(results["metrics"]["rouge2"]),
            "rougeL": np.mean(results["metrics"]["rougeL"]),
            "bleu": np.mean(results["metrics"]["bleu"]),
            "avg_tokens_per_second": np.mean([p["tokens_per_second"] for p in results["predictions"]]),
            "avg_generation_time": np.mean(results["metrics"]["generation_time"]),
            "total_samples": len(results["predictions"])
        }
    else:
        results["summary"] = {
            "avg_tokens_per_second": np.mean([p["tokens_per_second"] for p in results["predictions"]]),
            "avg_generation_time": np.mean(results["metrics"]["generation_time"]),
            "total_samples": len(results["predictions"])
        }
    
    # Print summary
    print("\n===== EVALUATION SUMMARY =====")
    for metric, value in results["summary"].items():
        print(f"{metric}: {value:.4f}" if isinstance(value, float) else f"{metric}: {value}")
    
    # Save results
    if output_file is None:
        output_file = f"sft_evaluation_results_{time.strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed results saved to {output_file}")
    return results

def tokenize_for_bleu(text):
    return nltk.word_tokenize(text.lower())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate a fine-tuned model")
    parser.add_argument("--model_path", type=str, default="./fine_tuned_model",
                      help="Path to the fine-tuned model")
    parser.add_argument("--evaluation_file", type=str, default=None,
                      help="Path to the evaluation JSONL file")
    parser.add_argument("--max_samples", type=int, default=None,
                      help="Maximum number of samples to evaluate")
    parser.add_argument("--max_new_tokens", type=int, default=200,
                      help="Maximum number of new tokens to generate")
    parser.add_argument("--output_file", type=str, default=None,
                      help="Path to save the evaluation results")
    
    args = parser.parse_args()
    evaluate_model(
        model_path=args.model_path,
        evaluation_file=args.evaluation_file,
        max_samples=args.max_samples,
        max_new_tokens=args.max_new_tokens,
        output_file=args.output_file
    )
