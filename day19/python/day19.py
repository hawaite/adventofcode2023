import os


class WorkflowOp:
    def __init__(self, workflow_op_string):
        if('>' in workflow_op_string or '<' in workflow_op_string):
            self.property_to_test = workflow_op_string[0]
            self.operator = workflow_op_string[1]

            value_and_target = workflow_op_string[2:].split(":")
            self.test_value = int(value_and_target[0])
            self.target_workflow = value_and_target[1]
        else:
            self.target_workflow = workflow_op_string
            self.test_value = None
            self.operator = None
            self.property_to_test = None

    def part_passes_operation(self, part):
        # unconditional jump operation
        if self.operator == None:
            return True
        
        if self.operator == '>':
            return part[self.property_to_test] > self.test_value
        elif self.operator == '<':
            return part[self.property_to_test] < self.test_value
        else:
            raise "Should never get here"

    def __repr__(self):
        return f"property to test: {self.property_to_test}, operator: {self.operator}, test value: {self.test_value}, target workflow: {self.target_workflow}"

def run_workflow_ops_on_part(workflow_operations:[WorkflowOp], part):
    for workflow_op in workflow_operations:
        result = workflow_op.part_passes_operation(part)
        if(result == True):
            # this is a match
            return workflow_op.target_workflow
        
    return None

def part_was_accepted(workflows_dict, current_workflow, part):
    workflow_result = run_workflow_ops_on_part(workflows_dict[current_workflow], part)
    if(workflow_result == 'A'):
        return True
    elif(workflow_result == 'R'):
        return False
    elif workflow_result != None:
        # found a new target workflow
        new_target = workflow_result
        return part_was_accepted(workflows_dict, new_target, part)
    else:
        raise "Should never get here"


def main():
    cwd = os.path.dirname(__file__)
    with(open(f"{cwd}/../input.txt", 'r') as fp):
        all_lines = fp.readlines()
    all_lines_trimmed = [x.strip() for x in all_lines]

    # parse workflows
    workflows = {}
    parts = []

    parsing_workflows = True
    for line in all_lines_trimmed:
        if line == "":
            parsing_workflows = False
            continue

        if parsing_workflows:
            workflow_name = line.split("{")[0]
            workflow_def = line.split("{")[1][:-1]

            workflow_defs = workflow_def.split(",")
            workflow_parts = []
            for wd in workflow_defs:
                workflow_parts.append(WorkflowOp(wd))
            workflows[workflow_name] = workflow_parts
        else:
            # parsing a part
            part = {}
            part_def = line[1:-1].split(",")
            for prop_def in part_def:
                segments = prop_def.split("=")
                part[segments[0]] = int(segments[1])

            parts.append(part)

    count = 0
    for part in parts:
        if part_was_accepted(workflows, "in", part):
            count += (part["x"] + part["m"] + part["a"] + part["s"])

    print(f"count -> {count}")
if __name__ == "__main__":
    main()