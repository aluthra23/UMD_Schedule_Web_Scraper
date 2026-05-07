from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("gpt2")
specials = ["<SEM>"] + [f"<INT_{i}>" for i in range(5)]  # or e.g. "<INT_Theory>"
# plus all of your course‑codes as “atomic” tokens:
course_tokens = ["CMSC131", "CMSC132",]

tokenizer.add_special_tokens({
    "additional_special_tokens": specials + course_tokens
})
