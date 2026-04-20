package com.school.school_management.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.school.school_management.dto.StudentRequest;
import com.school.school_management.entity.Student;
import java.util.List;

public interface StudentService extends IService<Student> {
    void addStudent(StudentRequest request, Integer teacherId);
    void updateStudent(Integer id, StudentRequest request, Integer currentUserId, Integer currentRole);
    void deleteStudent(Integer id, Integer currentUserId, Integer currentRole);
    Student getStudentById(Integer id, Integer currentUserId, Integer currentRole);
    List<Student> listStudents(Integer currentUserId, Integer currentRole, Integer teacherIdParam);
}