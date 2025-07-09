
a = int(input())
while (a>0):

    matrix = []

    # User Input arena
    for i in range(10):
        row = []
        row = list(input().strip())
        matrix.append(row)

    # Starter and storage variables
    left = 0
    right = 9
    top = 0
    bottom = 9
    
    
    score = 0
    factor = 1

    # Spiral traversal of Matrix
    while ((left <= right) and (top <= bottom)):
        counts = 0
        for i in range(left, right + 1):
            if(matrix[top][i] == "X"):
                counts += 1
        top += 1

        for i in range(top, bottom + 1):
            if(matrix[i][right] == "X"):
                counts += 1
        right -= 1

        if top <= bottom:
            for i in range(right, left - 1, -1):
                if(matrix[bottom][i] == "X"):
                    counts += 1
            bottom -= 1

        if left <= right:
            for i in range(bottom, top - 1, -1):
                if(matrix[i][left] == "X"):
                    counts += 1
            left += 1
        
        score += counts * (factor)
        factor += 1
        
    print(score)

    a -= 1