package com.school.school_management.service;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.school.school_management.dto.StudentRequest;
import com.school.school_management.entity.Student;
import com.school.school_management.mapper.StudentMapper;
import com.school.school_management.service.StudentService;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class StudentServiceImpl extends ServiceImpl<StudentMapper, Student> implements StudentService {

    @Override
    public void addStudent(StudentRequest request, Integer teacherId) {
        Student student = new Student();
        student.setName(request.getName());
        student.setGender(request.getGender());
        student.setAge(request.getAge());
        student.setClassName(request.getClassName());
        student.setTeacherId(teacherId);
        this.save(student);
    }

    @Override
    public void updateStudent(Integer id, StudentRequest request, Integer currentUserId, Integer currentRole) {
        Student student = this.getById(id);
        if (student == null) throw new RuntimeException("学生不存在");
        if (currentRole != 1 && !student.getTeacherId().equals(currentUserId)) {
            throw new RuntimeException("无权限修改此学生信息");
        }
        student.setName(request.getName());
        student.setGender(request.getGender());
        student.setAge(request.getAge());
        student.setClassName(request.getClassName());
        this.updateById(student);
    }

    @Override
    public void deleteStudent(Integer id, Integer currentUserId, Integer currentRole) {
        Student student = this.getById(id);
        if (student == null) throw new RuntimeException("学生不存在");
        if (currentRole != 1 && !student.getTeacherId().equals(currentUserId)) {
            throw new RuntimeException("无权限删除此学生");
        }
        this.removeById(id);
    }

    @Override
    public Student getStudentById(Integer id, Integer currentUserId, Integer currentRole) {
        Student student = this.getById(id);
        if (student == null) throw new RuntimeException("学生不存在");
        if (currentRole != 1 && !student.getTeacherId().equals(currentUserId)) {
            throw new RuntimeException("无权限查看此学生");
        }
        return student;
    }

    @Override
    public List<Student> listStudents(Integer currentUserId, Integer currentRole, Integer teacherIdParam) {
        LambdaQueryWrapper<Student> wrapper = new LambdaQueryWrapper<>();
        if (currentRole == 1) {
            if (teacherIdParam != null) {
                wrapper.eq(Student::getTeacherId, teacherIdParam);
            }
        } else {
            wrapper.eq(Student::getTeacherId, currentUserId);
        }
        wrapper.orderByDesc(Student::getCreateTime);
        return this.list(wrapper);
    }
}