package com.school.school_management.controller;

import com.school.school_management.dto.StudentRequest;
import com.school.school_management.entity.Student;
import com.school.school_management.service.StudentService;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/students")
public class StudentController {

    @Autowired
    private StudentService studentService;

    @PostMapping
    public String addStudent(@Valid @RequestBody StudentRequest request, HttpServletRequest httpRequest) {
        Integer teacherId = (Integer) httpRequest.getAttribute("userId");
        studentService.addStudent(request, teacherId);
        return "添加成功";
    }

    @PutMapping("/{id}")
    public String updateStudent(@PathVariable Integer id,
                                @Valid @RequestBody StudentRequest request,
                                HttpServletRequest httpRequest) {
        Integer userId = (Integer) httpRequest.getAttribute("userId");
        Integer role = (Integer) httpRequest.getAttribute("role");
        studentService.updateStudent(id, request, userId, role);
        return "修改成功";
    }

    @DeleteMapping("/{id}")
    public String deleteStudent(@PathVariable Integer id, HttpServletRequest httpRequest) {
        Integer userId = (Integer) httpRequest.getAttribute("userId");
        Integer role = (Integer) httpRequest.getAttribute("role");
        studentService.deleteStudent(id, userId, role);
        return "删除成功";
    }

    @GetMapping("/{id}")
    public Student getStudent(@PathVariable Integer id, HttpServletRequest httpRequest) {
        Integer userId = (Integer) httpRequest.getAttribute("userId");
        Integer role = (Integer) httpRequest.getAttribute("role");
        return studentService.getStudentById(id, userId, role);
    }

    @GetMapping
    public List<Student> listStudents(@RequestParam(required = false) Integer teacherId,
                                      HttpServletRequest httpRequest) {
        Integer userId = (Integer) httpRequest.getAttribute("userId");
        Integer role = (Integer) httpRequest.getAttribute("role");
        return studentService.listStudents(userId, role, teacherId);
    }
}
