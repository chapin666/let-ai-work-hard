# Source: chapter-05-cot-structured-output.md
# Lines: 27-50
# Language: javascript

// AI生成的简单实现
function generateSchedule(employees, shifts) {
  const schedule = {};
  
  for (let day = 0; day < 7; day++) {
    schedule[day] = {};
    
    for (const shift of shifts) {
      // 找第一个可用的员工
      const availableEmployee = employees.find(e => 
        e.availableDays.includes(day) && 
        e.skills.includes(shift.requiredSkill)
      );
      
      if (availableEmployee) {
        schedule[day][shift.id] = availableEmployee.id;
      }
    }
  }
  
  return schedule;
}
