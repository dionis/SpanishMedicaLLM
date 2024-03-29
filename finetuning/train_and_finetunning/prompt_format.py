import numpy as np


def format_prompt_meditron(prompt, args):
    if args.shots > 0:
        prompt = prompt[:-1]
    if "orca" in args.checkpoint_name:
        system_msg = "You are an AI assistant who helps people find information."
        return f"<|im_start|> system\n{system_msg}<|im_end|>\n<|im_start|> question\n{prompt}<|im_end|>\n<|im_start|> answer\n"
    elif "medical" in args.checkpoint_name:
        system_msg = "You are a helpful, respectful and honest assistant." + \
        "Always answer as helpfully as possible, while being safe." + \
        "Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content." + \
        "Please ensure that your responses are socially unbiased and positive in nature.\n\n" + \
        "If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct." + \
        "If you don't know the answer to a question, please don't share false information."""
        return f"<|im_start|> system\n{system_msg}<|im_end|>\n <|im_start|> user\n{prompt}<|im_end|>\n <|im_start|> assistant\n"
    elif np.any([x in args.checkpoint_name for x in ["medmcqa", "medqa", "pubmedqa"]]):
        return f"<|im_start|>question\n{prompt}<|im_end|>\n<|im_start|>answer\n"
    elif "med42" in args.checkpoint_name:
        if "Question:" in prompt:
            question = prompt.split("Question:")[1].strip()
        else:
            question = prompt
        return f'''\n<|system|>: You are a helpful medical assistant created by M42 Health in the UAE.\n<|prompter|>:{question}\n<|assistant|>:'''
    else:
        return prompt